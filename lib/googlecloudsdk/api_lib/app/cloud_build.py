
# Copyright 2013 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Utility methods to upload source to GCS and call Cloud Build service."""

import gzip
import os
import tempfile

from docker import docker
from googlecloudsdk.api_lib.app import cloud_storage
from googlecloudsdk.api_lib.app.api import operations
from googlecloudsdk.core import exceptions
from googlecloudsdk.core import log
from googlecloudsdk.core import properties
from googlecloudsdk.core.util import files
from googlecloudsdk.third_party.apis.cloudbuild import v1 as cloudbuild_v1


CLOUDBUILD_SUCCESS = 'SUCCESS'
CLOUDBUILD_LOGS_URI_TEMPLATE = (
    'https://console.developers.google.com/logs?project={project_id}'
    '&service=cloudbuild.googleapis.com&key1={build_id}')
CLOUDBUILD_LOGFILE_FMT_STRING = 'log-{build_id}.txt'

# Paths that shouldn't be ignored client-side.
# Behavioral parity with github.com/docker/docker-py.
BLACKLISTED_DOCKERIGNORE_PATHS = ['Dockerfile', '.dockerignore']


class UploadFailedError(exceptions.Error):
  """Raised when the source fails to upload to GCS."""


class BuildFailedError(exceptions.Error):
  """Raised when a Google Cloud Builder build fails."""


# This class is a workaround for the fact that the last line of
# docker.utils.tar does "fileobj.seek(0)" and gzip fails to seek in write mode,
# throwing "IOError: Negative seek in write mode".
class _GzipFileIgnoreSeek(gzip.GzipFile):
  """Wrapper around GzipFile that ignores seek requests."""

  def seek(self, offset, whence=0):
    return self.offset


def UploadSource(source_dir, bucket, obj, storage_client):
  """Upload a gzipped tarball of the source directory to GCS.

  Note: To provide parity with docker's behavior, we must respect .dockerignore.

  Args:
    source_dir: the directory to be archived.
    bucket: the GCS bucket where the tarball will be stored.
    obj: the GCS object where the tarball will be stored, in the above bucket.
    storage_client: An instance of the storage_v1.StorageV1 client.

  Raises:
    UploadFailedError: when the source fails to upload to GCS.
  """
  dockerignore = os.path.join(source_dir, '.dockerignore')
  exclude = None
  if os.path.exists(dockerignore):
    with open(dockerignore) as f:
      # Read the exclusions, filtering out blank lines.
      exclude = set(filter(bool, f.read().splitlines()))
      # Remove paths that shouldn't be excluded on the client.
      exclude -= set(BLACKLISTED_DOCKERIGNORE_PATHS)
  # We can't use tempfile.NamedTemporaryFile here because ... Windows.
  # See https://bugs.python.org/issue14243. There are small cleanup races
  # during process termination that will leave artifacts on the filesystem.
  # eg, CTRL-C on windows leaves both the directory and the file. Unavoidable.
  # On Posix, `kill -9` has similar behavior, but CTRL-C allows cleanup.
  try:
    temp_dir = tempfile.mkdtemp()
    f = open(os.path.join(temp_dir, 'src.tgz'), 'w+b')
    # We are able to leverage the source archiving code from docker-py;
    # however, there are two wrinkles:
    # 1) The 3P code doesn't support gzip (it's expecting a local unix socket).
    #    So we create a GzipFile object and let the 3P code write into that.
    # 2) The .seek(0) call at the end of the 3P code causes GzipFile to throw an
    #    exception. So we use GzipFileIgnoreSeek as a workaround.
    with _GzipFileIgnoreSeek(mode='wb', fileobj=f) as gz:
      docker.utils.tar(source_dir, exclude, fileobj=gz)
    f.close()
    cloud_storage.CopyFileToGCS(bucket, f.name, obj, storage_client)
  finally:
    try:
      files.RmTree(temp_dir)
    except OSError:
      log.warn('Could not remove temporary directory [{0}]'.format(temp_dir))


def ExecuteCloudBuild(project, bucket_ref, object_name, output_image,
                      cloudbuild_client, http):
  """Execute a call to CloudBuild service and wait for it to finish.

  Args:
    project: the cloud project ID.
    bucket_ref: Reference to GCS bucket containing source to build.
    object_name: GCS object name containing source to build.
    output_image: GCR location for the output docker image;
                  eg, gcr.io/test-gae/hardcoded-output-tag.
    cloudbuild_client: client to the Cloud Build service.
    http: an http provider that can be used to create api clients.

  Raises:
    BuildFailedError: when the build fails.
  """
  builder = properties.VALUES.app.container_builder_image.Get()
  log.debug('Using builder image: [{0}]'.format(builder))
  logs_bucket = bucket_ref.bucket
  build_op = cloudbuild_client.projects_builds.Create(
      cloudbuild_v1.CloudbuildProjectsBuildsCreateRequest(
          projectId=project,
          build=cloudbuild_v1.Build(
              source=cloudbuild_v1.Source(
                  storageSource=cloudbuild_v1.StorageSource(
                      bucket=bucket_ref.bucket,
                      object=object_name,
                  ),
              ),
              steps=[cloudbuild_v1.BuildStep(
                  name=builder,
                  args=[output_image]
              )],
              images=[output_image],
              logsBucket=logs_bucket,
          ),
      )
  )
  # Find build ID from operation metadata and print the logs URL.
  build_id = None
  if build_op.metadata is not None:
    for prop in build_op.metadata.additionalProperties:
      if prop.key == 'build':
        for build_prop in prop.value.object_value.properties:
          if build_prop.key == 'id':
            build_id = build_prop.value.string_value
            break
        break

  if build_id is None:
    raise BuildFailedError('Could not determine build ID')
  log.status.Print(
      'Started cloud build [{build_id}].'.format(build_id=build_id))
  log_object = CLOUDBUILD_LOGFILE_FMT_STRING.format(build_id=build_id)
  log_tailer = cloud_storage.LogTailer(
      http=http,
      bucket=logs_bucket,
      obj=log_object)
  logs_uri = CLOUDBUILD_LOGS_URI_TEMPLATE.format(project_id=project,
                                                 build_id=build_id)
  log.status.Print('To see logs in the Cloud Console: ' + logs_uri)
  op = operations.WaitForOperation(
      operation_service=cloudbuild_client.operations,
      operation=build_op,
      retry_interval=1,
      max_retries=60 * 60,
      retry_callback=log_tailer.Poll)
  # Poll the logs one final time to ensure we have everything. We know this
  # final poll will get the full log contents because GCS is strongly consistent
  # and Container Builder waits for logs to finish pushing before marking the
  # build complete.
  log_tailer.Poll(is_last=True)
  final_status = _GetStatusFromOp(op)
  if final_status != CLOUDBUILD_SUCCESS:
    raise BuildFailedError('Cloud build failed with status '
                           + final_status + '. Check logs at ' + logs_uri)


def _GetStatusFromOp(op):
  """Get the Cloud Build Status from an Operation object.

  The op.response field is supposed to have a copy of the build object; however,
  the wire JSON from the server doesn't get deserialized into an actual build
  object. Instead, it is stored as a generic ResponseValue object, so we have
  to root around a bit.

  Args:
    op: the Operation object from a CloudBuild build request.

  Returns:
    string status, likely "SUCCESS" or "ERROR".
  """
  for prop in op.response.additionalProperties:
    if prop.key == 'status':
      return prop.value.string_value
  return 'UNKNOWN'
