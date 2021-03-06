"""Generated message classes for sourcerepo version v1.

Accesses source code repositories hosted by Google.
"""
# NOTE: This file is autogenerated and should not be edited by hand.

from apitools.base.protorpclite import messages as _messages
from apitools.base.py import encoding


package = 'sourcerepo'


class AuditConfig(_messages.Message):
  r"""Specifies the audit configuration for a service. The configuration
  determines which permission types are logged, and what identities, if any,
  are exempted from logging. An AuditConfig must have one or more
  AuditLogConfigs.  If there are AuditConfigs for both `allServices` and a
  specific service, the union of the two AuditConfigs is used for that
  service: the log_types specified in each AuditConfig are enabled, and the
  exempted_members in each AuditLogConfig are exempted.  Example Policy with
  multiple AuditConfigs:      {       "audit_configs": [         {
  "service": "allServices"           "audit_log_configs": [             {
  "log_type": "DATA_READ",               "exempted_members": [
  "user:foo@gmail.com"               ]             },             {
  "log_type": "DATA_WRITE",             },             {
  "log_type": "ADMIN_READ",             }           ]         },         {
  "service": "fooservice.googleapis.com"           "audit_log_configs": [
  {               "log_type": "DATA_READ",             },             {
  "log_type": "DATA_WRITE",               "exempted_members": [
  "user:bar@gmail.com"               ]             }           ]         }
  ]     }  For fooservice, this policy enables DATA_READ, DATA_WRITE and
  ADMIN_READ logging. It also exempts foo@gmail.com from DATA_READ logging,
  and bar@gmail.com from DATA_WRITE logging.

  Fields:
    auditLogConfigs: The configuration for logging of each type of permission.
    service: Specifies a service that will be enabled for audit logging. For
      example, `storage.googleapis.com`, `cloudsql.googleapis.com`.
      `allServices` is a special value that covers all services.
  """

  auditLogConfigs = _messages.MessageField('AuditLogConfig', 1, repeated=True)
  service = _messages.StringField(2)


class AuditLogConfig(_messages.Message):
  r"""Provides the configuration for logging a type of permissions. Example:
  {       "audit_log_configs": [         {           "log_type": "DATA_READ",
  "exempted_members": [             "user:foo@gmail.com"           ]
  },         {           "log_type": "DATA_WRITE",         }       ]     }
  This enables 'DATA_READ' and 'DATA_WRITE' logging, while exempting
  foo@gmail.com from DATA_READ logging.

  Enums:
    LogTypeValueValuesEnum: The log type that this config enables.

  Fields:
    exemptedMembers: Specifies the identities that do not cause logging for
      this type of permission. Follows the same format of Binding.members.
    logType: The log type that this config enables.
  """

  class LogTypeValueValuesEnum(_messages.Enum):
    r"""The log type that this config enables.

    Values:
      LOG_TYPE_UNSPECIFIED: Default case. Should never be this.
      ADMIN_READ: Admin reads. Example: CloudIAM getIamPolicy
      DATA_WRITE: Data writes. Example: CloudSQL Users create
      DATA_READ: Data reads. Example: CloudSQL Users list
    """
    LOG_TYPE_UNSPECIFIED = 0
    ADMIN_READ = 1
    DATA_WRITE = 2
    DATA_READ = 3

  exemptedMembers = _messages.StringField(1, repeated=True)
  logType = _messages.EnumField('LogTypeValueValuesEnum', 2)


class Binding(_messages.Message):
  r"""Associates `members` with a `role`.

  Fields:
    condition: Unimplemented. The condition that is associated with this
      binding. NOTE: an unsatisfied condition will not allow user access via
      current binding. Different bindings, including their conditions, are
      examined independently.
    members: Specifies the identities requesting access for a Cloud Platform
      resource. `members` can have the following values:  * `allUsers`: A
      special identifier that represents anyone who is    on the internet;
      with or without a Google account.  * `allAuthenticatedUsers`: A special
      identifier that represents anyone    who is authenticated with a Google
      account or a service account.  * `user:{emailid}`: An email address that
      represents a specific Google    account. For example, `alice@gmail.com`
      .   * `serviceAccount:{emailid}`: An email address that represents a
      service    account. For example, `my-other-
      app@appspot.gserviceaccount.com`.  * `group:{emailid}`: An email address
      that represents a Google group.    For example, `admins@example.com`.
      * `domain:{domain}`: The G Suite domain (primary) that represents all
      the    users of that domain. For example, `google.com` or `example.com`.
    role: Role that is assigned to `members`. For example, `roles/viewer`,
      `roles/editor`, or `roles/owner`.
  """

  condition = _messages.MessageField('Expr', 1)
  members = _messages.StringField(2, repeated=True)
  role = _messages.StringField(3)


class Empty(_messages.Message):
  r"""A generic empty message that you can re-use to avoid defining duplicated
  empty messages in your APIs. A typical example is to use it as the request
  or the response type of an API method. For instance:      service Foo {
  rpc Bar(google.protobuf.Empty) returns (google.protobuf.Empty);     }  The
  JSON representation for `Empty` is empty JSON object `{}`.
  """



class Expr(_messages.Message):
  r"""Represents an expression text. Example:      title: "User account
  presence"     description: "Determines whether the request has a user
  account"     expression: "size(request.user) > 0"

  Fields:
    description: An optional description of the expression. This is a longer
      text which describes the expression, e.g. when hovered over it in a UI.
    expression: Textual representation of an expression in Common Expression
      Language syntax.  The application context of the containing message
      determines which well-known feature set of CEL is supported.
    location: An optional string indicating the location of the expression for
      error reporting, e.g. a file name and a position in the file.
    title: An optional title for the expression, i.e. a short string
      describing its purpose. This can be used e.g. in UIs which allow to
      enter the expression.
  """

  description = _messages.StringField(1)
  expression = _messages.StringField(2)
  location = _messages.StringField(3)
  title = _messages.StringField(4)


class ListReposResponse(_messages.Message):
  r"""Response for ListRepos.  The size is not set in the returned
  repositories.

  Fields:
    nextPageToken: If non-empty, additional repositories exist within the
      project. These can be retrieved by including this value in the next
      ListReposRequest's page_token field.
    repos: The listed repos.
  """

  nextPageToken = _messages.StringField(1)
  repos = _messages.MessageField('Repo', 2, repeated=True)


class MirrorConfig(_messages.Message):
  r"""Configuration to automatically mirror a repository from another hosting
  service, for example GitHub or Bitbucket.

  Fields:
    deployKeyId: ID of the SSH deploy key at the other hosting service.
      Removing this key from the other service would deauthorize Google Cloud
      Source Repositories from mirroring.
    url: URL of the main repository at the other hosting service.
    webhookId: ID of the webhook listening to updates to trigger mirroring.
      Removing this webhook from the other hosting service will stop Google
      Cloud Source Repositories from receiving notifications, and thereby
      disabling mirroring.
  """

  deployKeyId = _messages.StringField(1)
  url = _messages.StringField(2)
  webhookId = _messages.StringField(3)


class Policy(_messages.Message):
  r"""Defines an Identity and Access Management (IAM) policy. It is used to
  specify access control policies for Cloud Platform resources.   A `Policy`
  consists of a list of `bindings`. A `binding` binds a list of `members` to a
  `role`, where the members can be user accounts, Google groups, Google
  domains, and service accounts. A `role` is a named list of permissions
  defined by IAM.  **JSON Example**      {       "bindings": [         {
  "role": "roles/owner",           "members": [
  "user:mike@example.com",             "group:admins@example.com",
  "domain:google.com",             "serviceAccount:my-other-
  app@appspot.gserviceaccount.com"           ]         },         {
  "role": "roles/viewer",           "members": ["user:sean@example.com"]
  }       ]     }  **YAML Example**      bindings:     - members:       -
  user:mike@example.com       - group:admins@example.com       -
  domain:google.com       - serviceAccount:my-other-
  app@appspot.gserviceaccount.com       role: roles/owner     - members:
  - user:sean@example.com       role: roles/viewer   For a description of IAM
  and its features, see the [IAM developer's
  guide](https://cloud.google.com/iam/docs).

  Fields:
    auditConfigs: Specifies cloud audit logging configuration for this policy.
    bindings: Associates a list of `members` to a `role`. `bindings` with no
      members will result in an error.
    etag: `etag` is used for optimistic concurrency control as a way to help
      prevent simultaneous updates of a policy from overwriting each other. It
      is strongly suggested that systems make use of the `etag` in the read-
      modify-write cycle to perform policy updates in order to avoid race
      conditions: An `etag` is returned in the response to `getIamPolicy`, and
      systems are expected to put that etag in the request to `setIamPolicy`
      to ensure that their change will be applied to the same version of the
      policy.  If no `etag` is provided in the call to `setIamPolicy`, then
      the existing policy is overwritten blindly.
    version: Deprecated.
  """

  auditConfigs = _messages.MessageField('AuditConfig', 1, repeated=True)
  bindings = _messages.MessageField('Binding', 2, repeated=True)
  etag = _messages.BytesField(3)
  version = _messages.IntegerField(4, variant=_messages.Variant.INT32)


class ProjectConfig(_messages.Message):
  r"""Cloud Source Repositories configuration of a project.

  Messages:
    PubsubConfigsValue: How this project publishes a change in the
      repositories through Cloud Pub/Sub. Keyed by the topic names.

  Fields:
    enablePrivateKeyCheck: Reject a Git push that contains a private key.
    name: The name of the project. Values are of the form
      `projects/<project>`.
    pubsubConfigs: How this project publishes a change in the repositories
      through Cloud Pub/Sub. Keyed by the topic names.
  """

  @encoding.MapUnrecognizedFields('additionalProperties')
  class PubsubConfigsValue(_messages.Message):
    r"""How this project publishes a change in the repositories through Cloud
    Pub/Sub. Keyed by the topic names.

    Messages:
      AdditionalProperty: An additional property for a PubsubConfigsValue
        object.

    Fields:
      additionalProperties: Additional properties of type PubsubConfigsValue
    """

    class AdditionalProperty(_messages.Message):
      r"""An additional property for a PubsubConfigsValue object.

      Fields:
        key: Name of the additional property.
        value: A PubsubConfig attribute.
      """

      key = _messages.StringField(1)
      value = _messages.MessageField('PubsubConfig', 2)

    additionalProperties = _messages.MessageField('AdditionalProperty', 1, repeated=True)

  enablePrivateKeyCheck = _messages.BooleanField(1)
  name = _messages.StringField(2)
  pubsubConfigs = _messages.MessageField('PubsubConfigsValue', 3)


class PubsubConfig(_messages.Message):
  r"""Configuration to publish a Cloud Pub/Sub message.

  Enums:
    MessageFormatValueValuesEnum: The format of the Cloud Pub/Sub messages.

  Fields:
    messageFormat: The format of the Cloud Pub/Sub messages.
    serviceAccountEmail: Email address of the service account used for
      publishing Cloud Pub/Sub messages. This service account needs to be in
      the same project as the PubsubConfig. When added, the caller needs to
      have iam.serviceAccounts.actAs permission on this service account. If
      unspecified, it defaults to the compute engine default service account.
    topic: A topic of Cloud Pub/Sub. Values are of the form
      `projects/<project>/topics/<topic>`. The project needs to be the same
      project as this config is in.
  """

  class MessageFormatValueValuesEnum(_messages.Enum):
    r"""The format of the Cloud Pub/Sub messages.

    Values:
      MESSAGE_FORMAT_UNSPECIFIED: Unspecified.
      PROTOBUF: The message payload is a serialized protocol buffer of
        SourceRepoEvent.
      JSON: The message payload is a JSON string of SourceRepoEvent.
    """
    MESSAGE_FORMAT_UNSPECIFIED = 0
    PROTOBUF = 1
    JSON = 2

  messageFormat = _messages.EnumField('MessageFormatValueValuesEnum', 1)
  serviceAccountEmail = _messages.StringField(2)
  topic = _messages.StringField(3)


class Repo(_messages.Message):
  r"""A repository (or repo) is a Git repository storing versioned source
  content.

  Messages:
    PubsubConfigsValue: How this repository publishes a change in the
      repository through Cloud Pub/Sub. Keyed by the topic names.

  Fields:
    mirrorConfig: How this repository mirrors a repository managed by another
      service. Read-only field.
    name: Resource name of the repository, of the form
      `projects/<project>/repos/<repo>`.  The repo name may contain slashes.
      eg, `projects/myproject/repos/name/with/slash`
    pubsubConfigs: How this repository publishes a change in the repository
      through Cloud Pub/Sub. Keyed by the topic names.
    size: The disk usage of the repo, in bytes. Read-only field. Size is only
      returned by GetRepo.
    url: URL to clone the repository from Google Cloud Source Repositories.
      Read-only field.
  """

  @encoding.MapUnrecognizedFields('additionalProperties')
  class PubsubConfigsValue(_messages.Message):
    r"""How this repository publishes a change in the repository through Cloud
    Pub/Sub. Keyed by the topic names.

    Messages:
      AdditionalProperty: An additional property for a PubsubConfigsValue
        object.

    Fields:
      additionalProperties: Additional properties of type PubsubConfigsValue
    """

    class AdditionalProperty(_messages.Message):
      r"""An additional property for a PubsubConfigsValue object.

      Fields:
        key: Name of the additional property.
        value: A PubsubConfig attribute.
      """

      key = _messages.StringField(1)
      value = _messages.MessageField('PubsubConfig', 2)

    additionalProperties = _messages.MessageField('AdditionalProperty', 1, repeated=True)

  mirrorConfig = _messages.MessageField('MirrorConfig', 1)
  name = _messages.StringField(2)
  pubsubConfigs = _messages.MessageField('PubsubConfigsValue', 3)
  size = _messages.IntegerField(4)
  url = _messages.StringField(5)


class SetIamPolicyRequest(_messages.Message):
  r"""Request message for `SetIamPolicy` method.

  Fields:
    policy: REQUIRED: The complete policy to be applied to the `resource`. The
      size of the policy is limited to a few 10s of KB. An empty policy is a
      valid policy but certain Cloud Platform services (such as Projects)
      might reject them.
    updateMask: OPTIONAL: A FieldMask specifying which fields of the policy to
      modify. Only the fields in the mask will be modified. If no mask is
      provided, the following default mask is used: paths: "bindings, etag"
      This field is only used by Cloud IAM.
  """

  policy = _messages.MessageField('Policy', 1)
  updateMask = _messages.StringField(2)


class SourcerepoProjectsGetConfigRequest(_messages.Message):
  r"""A SourcerepoProjectsGetConfigRequest object.

  Fields:
    name: The name of the requested project. Values are of the form
      `projects/<project>`.
  """

  name = _messages.StringField(1, required=True)


class SourcerepoProjectsReposCreateRequest(_messages.Message):
  r"""A SourcerepoProjectsReposCreateRequest object.

  Fields:
    parent: The project in which to create the repo. Values are of the form
      `projects/<project>`.
    repo: A Repo resource to be passed as the request body.
  """

  parent = _messages.StringField(1, required=True)
  repo = _messages.MessageField('Repo', 2)


class SourcerepoProjectsReposDeleteRequest(_messages.Message):
  r"""A SourcerepoProjectsReposDeleteRequest object.

  Fields:
    name: The name of the repo to delete. Values are of the form
      `projects/<project>/repos/<repo>`.
  """

  name = _messages.StringField(1, required=True)


class SourcerepoProjectsReposGetIamPolicyRequest(_messages.Message):
  r"""A SourcerepoProjectsReposGetIamPolicyRequest object.

  Fields:
    resource: REQUIRED: The resource for which the policy is being requested.
      See the operation documentation for the appropriate value for this
      field.
  """

  resource = _messages.StringField(1, required=True)


class SourcerepoProjectsReposGetRequest(_messages.Message):
  r"""A SourcerepoProjectsReposGetRequest object.

  Fields:
    name: The name of the requested repository. Values are of the form
      `projects/<project>/repos/<repo>`.
  """

  name = _messages.StringField(1, required=True)


class SourcerepoProjectsReposListRequest(_messages.Message):
  r"""A SourcerepoProjectsReposListRequest object.

  Fields:
    name: The project ID whose repos should be listed. Values are of the form
      `projects/<project>`.
    pageSize: Maximum number of repositories to return; between 1 and 500. If
      not set or zero, defaults to 100 at the server.
    pageToken: Resume listing repositories where a prior ListReposResponse
      left off. This is an opaque token that must be obtained from a recent,
      prior ListReposResponse's next_page_token field.
  """

  name = _messages.StringField(1, required=True)
  pageSize = _messages.IntegerField(2, variant=_messages.Variant.INT32)
  pageToken = _messages.StringField(3)


class SourcerepoProjectsReposPatchRequest(_messages.Message):
  r"""A SourcerepoProjectsReposPatchRequest object.

  Fields:
    name: The name of the requested repository. Values are of the form
      `projects/<project>/repos/<repo>`.
    updateRepoRequest: A UpdateRepoRequest resource to be passed as the
      request body.
  """

  name = _messages.StringField(1, required=True)
  updateRepoRequest = _messages.MessageField('UpdateRepoRequest', 2)


class SourcerepoProjectsReposSetIamPolicyRequest(_messages.Message):
  r"""A SourcerepoProjectsReposSetIamPolicyRequest object.

  Fields:
    resource: REQUIRED: The resource for which the policy is being specified.
      See the operation documentation for the appropriate value for this
      field.
    setIamPolicyRequest: A SetIamPolicyRequest resource to be passed as the
      request body.
  """

  resource = _messages.StringField(1, required=True)
  setIamPolicyRequest = _messages.MessageField('SetIamPolicyRequest', 2)


class SourcerepoProjectsReposTestIamPermissionsRequest(_messages.Message):
  r"""A SourcerepoProjectsReposTestIamPermissionsRequest object.

  Fields:
    resource: REQUIRED: The resource for which the policy detail is being
      requested. See the operation documentation for the appropriate value for
      this field.
    testIamPermissionsRequest: A TestIamPermissionsRequest resource to be
      passed as the request body.
  """

  resource = _messages.StringField(1, required=True)
  testIamPermissionsRequest = _messages.MessageField('TestIamPermissionsRequest', 2)


class SourcerepoProjectsUpdateConfigRequest(_messages.Message):
  r"""A SourcerepoProjectsUpdateConfigRequest object.

  Fields:
    name: The name of the requested project. Values are of the form
      `projects/<project>`.
    updateProjectConfigRequest: A UpdateProjectConfigRequest resource to be
      passed as the request body.
  """

  name = _messages.StringField(1, required=True)
  updateProjectConfigRequest = _messages.MessageField('UpdateProjectConfigRequest', 2)


class StandardQueryParameters(_messages.Message):
  r"""Query parameters accepted by all methods.

  Enums:
    FXgafvValueValuesEnum: V1 error format.
    AltValueValuesEnum: Data format for response.

  Fields:
    f__xgafv: V1 error format.
    access_token: OAuth access token.
    alt: Data format for response.
    callback: JSONP
    fields: Selector specifying which fields to include in a partial response.
    key: API key. Your API key identifies your project and provides you with
      API access, quota, and reports. Required unless you provide an OAuth 2.0
      token.
    oauth_token: OAuth 2.0 token for the current user.
    prettyPrint: Returns response with indentations and line breaks.
    quotaUser: Available to use for quota purposes for server-side
      applications. Can be any arbitrary string assigned to a user, but should
      not exceed 40 characters.
    trace: A tracing token of the form "token:<tokenid>" to include in api
      requests.
    uploadType: Legacy upload protocol for media (e.g. "media", "multipart").
    upload_protocol: Upload protocol for media (e.g. "raw", "multipart").
  """

  class AltValueValuesEnum(_messages.Enum):
    r"""Data format for response.

    Values:
      json: Responses with Content-Type of application/json
      media: Media download with context-dependent Content-Type
      proto: Responses with Content-Type of application/x-protobuf
    """
    json = 0
    media = 1
    proto = 2

  class FXgafvValueValuesEnum(_messages.Enum):
    r"""V1 error format.

    Values:
      _1: v1 error format
      _2: v2 error format
    """
    _1 = 0
    _2 = 1

  f__xgafv = _messages.EnumField('FXgafvValueValuesEnum', 1)
  access_token = _messages.StringField(2)
  alt = _messages.EnumField('AltValueValuesEnum', 3, default=u'json')
  callback = _messages.StringField(4)
  fields = _messages.StringField(5)
  key = _messages.StringField(6)
  oauth_token = _messages.StringField(7)
  prettyPrint = _messages.BooleanField(8, default=True)
  quotaUser = _messages.StringField(9)
  trace = _messages.StringField(10)
  uploadType = _messages.StringField(11)
  upload_protocol = _messages.StringField(12)


class TestIamPermissionsRequest(_messages.Message):
  r"""Request message for `TestIamPermissions` method.

  Fields:
    permissions: The set of permissions to check for the `resource`.
      Permissions with wildcards (such as '*' or 'storage.*') are not allowed.
      For more information see [IAM
      Overview](https://cloud.google.com/iam/docs/overview#permissions).
  """

  permissions = _messages.StringField(1, repeated=True)


class TestIamPermissionsResponse(_messages.Message):
  r"""Response message for `TestIamPermissions` method.

  Fields:
    permissions: A subset of `TestPermissionsRequest.permissions` that the
      caller is allowed.
  """

  permissions = _messages.StringField(1, repeated=True)


class UpdateProjectConfigRequest(_messages.Message):
  r"""Request for UpdateProjectConfig.

  Fields:
    projectConfig: The new configuration for the project.
    updateMask: A FieldMask specifying which fields of the project_config to
      modify. Only the fields in the mask will be modified. If no mask is
      provided, this request is no-op.
  """

  projectConfig = _messages.MessageField('ProjectConfig', 1)
  updateMask = _messages.StringField(2)


class UpdateRepoRequest(_messages.Message):
  r"""Request for UpdateRepo.

  Fields:
    repo: The new configuration for the repository.
    updateMask: A FieldMask specifying which fields of the repo to modify.
      Only the fields in the mask will be modified. If no mask is provided,
      this request is no-op.
  """

  repo = _messages.MessageField('Repo', 1)
  updateMask = _messages.StringField(2)


encoding.AddCustomJsonFieldMapping(
    StandardQueryParameters, 'f__xgafv', '$.xgafv')
encoding.AddCustomJsonEnumMapping(
    StandardQueryParameters.FXgafvValueValuesEnum, '_1', '1')
encoding.AddCustomJsonEnumMapping(
    StandardQueryParameters.FXgafvValueValuesEnum, '_2', '2')
