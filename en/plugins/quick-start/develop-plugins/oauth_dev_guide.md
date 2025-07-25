# Adding OAuth to Your Tool Plugin

## Why OAuth Exists in Dify

[OAuth](https://oauth.net/2/) (Open Authorization) is a better way to authorize tool plugins that need to access user data from third-party services like Gmail or GitHub. Instead of requiring the user to manually enter API keys, OAuth provides a secure way to act on behalf of the user with their explicit consent. You can 

## Deployment Architecture First

Your OAuth implementation depends entirely on where Dify runs. Get this wrong and you'll waste days debugging redirect URIs.

### Dify Cloud (SaaS)

- **Dify manages OAuth apps** for verified plugins
- Users just click "Add OAuth" → authorize → done
- Your redirect URI: `https://cloud.dify.ai/console/api/oauth/plugin/{plugin-id}/{provider-name}/{tool-name}/callback`
- Zero OAuth app setup for users

### Self-Hosted

- **Users manage their own OAuth apps** (Google Cloud Console, GitHub Apps, etc.)
- Must configure client_id/client_secret before any OAuth works
- Your redirect URI: `https://their-domain.com/console/api/oauth/plugin/{plugin-id}/{provider-name}/{tool-name}/callback`
- Users see "Setup OAuth Client" button before they can authorize

### Custom Mode (SaaS override)

- Users can override Dify's managed keys with their own
- Same setup as Self-Hosted but optional

## Multi-Credential Reality

**Critical**: Dify supports multiple OAuth credentials per plugin. Users can have work Gmail \+ personal Gmail. Your plugin needs to handle this correctly.

**Default Logic**:

- First credential becomes "Default"
- Apps reference credentials by Default unless explicitly changed
- Users can change which credential is Default
- DSLs never store credential IDs (they stay portable)

**Mixed Auth Types**:
Plugins can offer both OAuth AND API-Key simultaneously. Users pick what works for their setup.

## Implementation

### 1. Define OAuth Schema in YAML

**Purpose**: Tell Dify what credentials your plugin needs and what the OAuth flow will produce.

**Two schemas required**:

#### client_schema

What users configure from their OAuth app:

```yaml
oauth_schema:
  client_schema:
    - name: "client_id"
      type: "secret-input"
      required: true
      url: "https://console.cloud.google.com/apis/credentials"
    - name: "client_secret"
      type: "secret-input" 
      required: true
```

**Critical**: The `url` field links directly to where users create OAuth apps. This saves support tickets.

#### credentials_schema

What OAuth produces (Dify manages these):

```yaml
  credentials_schema:
    - name: "access_token"
      type: "secret-input"
    - name: "refresh_token"
      type: "secret-input"
    - name: "expires_at"
      type: "secret-input"
```

**Mixed Auth Support**: Include both `oauth_schema` and `credentials_for_provider` to offer OAuth \+ API key options.

### 2. Implement Authorization URL Generation

**Purpose**: Create the URL where users grant permissions to your plugin.

```python
def _oauth_get_authorization_url(self, redirect_uri: str, system_credentials: Mapping[str, Any]) -> str:
    params = {
        "client_id": system_credentials["client_id"],
        "redirect_uri": redirect_uri,
        "scope": "user:email repo",
        "access_type": "offline",  # Gets refresh token
    }
    return f"https://github.com/login/oauth/authorize?{urllib.parse.urlencode(params)}"
```

**Input**:

- `redirect_uri`: Dify's callback URL (don't modify)
- `system_credentials`: Contains `client_id`, `client_secret` from user's OAuth app

**Output**: Complete authorization URL string

**Critical parameters**:

- `access_type=offline`: Required for refresh tokens
- `prompt=consent`: Forces reauth when scopes change

### 3. Exchange Code for Tokens

**Purpose**: Convert the authorization code into usable access tokens.

```python
def _oauth_get_credentials(self, redirect_uri: str, system_credentials: Mapping[str, Any], request: Request) -> ToolOAuthCredentials:
    code = request.args.get("code")
    
    response = requests.post("https://github.com/login/oauth/access_token", data={
        "client_id": system_credentials["client_id"],
        "client_secret": system_credentials["client_secret"],
        "code": code,
    }, headers={"Accept": "application/json"})
    
    tokens = response.json()
    expires_at = int(time.time() + tokens.get("expires_in", 3600))
    
    return ToolOAuthCredentials(
        credentials={"access_token": tokens["access_token"], "expires_at": expires_at},
        expires_at=expires_at
    )
```

**Input**:

- `request`: Contains authorization `code` in query parameters
- Same `redirect_uri` and `system_credentials` from step 2

**Output**: `ToolOAuthCredentials` object with:

- `credentials`: Dict containing tokens
- `expires_at`: Unix timestamp for token expiry

**Error handling**: Raise `ToolProviderOAuthError` if token exchange fails.

### 4. Handle Token Refresh

**Purpose**: Get new access tokens when current ones expire.

```python
def _oauth_refresh_credentials(self, redirect_uri: str, system_credentials: Mapping[str, Any], credentials: Mapping[str, Any]) -> ToolOAuthCredentials:
    response = requests.post("https://oauth.service.com/token", data={
        "grant_type": "refresh_token",
        "refresh_token": credentials["refresh_token"],
        "client_id": system_credentials["client_id"],
    })
    
    tokens = response.json()
    expires_at = int(time.time() + tokens["expires_in"])
    
    return ToolOAuthCredentials(
        credentials={"access_token": tokens["access_token"], "expires_at": expires_at},
        expires_at=expires_at
    )
```

**Input**:

- `credentials`: Current credentials containing `refresh_token`
- Same `system_credentials` from OAuth app

**Output**: New `ToolOAuthCredentials` with fresh `access_token`

**Note**: Some services don't provide refresh tokens. Handle gracefully.

### 5. Validate Credentials Work

**Purpose**: Test credentials by making a real API call.

```python
def _validate_credentials(self, credentials: dict[str, Any]) -> None:
    response = requests.get("https://api.github.com/user", 
                          headers={"Authorization": f"Bearer {credentials['access_token']}"})
    if response.status_code != 200:
        raise ToolProviderCredentialValidationError("Invalid credentials")
```

**Input**: Credentials dict containing `access_token`
**Output**: None (raises exception if invalid)

**Purpose**: Called when users connect and periodically to verify credentials still work.

### 6. Access Tokens in Your Tools

**Purpose**: Use OAuth credentials to make authenticated API calls.

```python
class YourTool(BuiltinTool):
    def _invoke(self, user_id: str, tool_parameters: dict[str, Any]) -> ToolInvokeMessage:
        access_token = self.runtime.credentials["access_token"]
        
        response = requests.get("https://api.service.com/data",
                              headers={"Authorization": f"Bearer {access_token}"})
        return self.create_text_message(response.text)
```

**Key**: `self.runtime.credentials` automatically provides the current user's tokens. Dify handles refresh automatically.

## OAuth App Setup by Service

### Google (Gmail, Drive, Calendar)

1. **Google Cloud Console** → Create Project
2. **APIs & Services** → Enable required APIs (Gmail, Drive, etc.)
3. **OAuth Consent Screen**:
   - External user type
   - Add test users during development
   - Submit for verification for production
4. **Credentials** → OAuth 2.0 Client ID:
   - Web application
   - Authorized redirect URIs: `https://your-dify-domain.com/console/api/oauth/plugin/{plugin-id}/{provider-name}/{tool-name}/callback`

### GitHub

1. **Settings** → Developer settings → OAuth Apps
2. **New OAuth App**:
   - Authorization callback URL: `https://your-dify-domain.com/console/api/oauth/plugin/{plugin-id}/{provider-name}/{tool-name}/callback`
   - Save Client ID and Client Secret

### Notion

1. **My integrations** → New integration
2. **OAuth Domain & URIs**:
   - Redirect URI: `https://your-dify-domain.com/console/api/oauth/plugin/{plugin-id}/{provider-name}/{tool-name}/callback`
3. **Capabilities**: Select required permissions

## Debugging OAuth Issues

### 403 Forbidden

**Root cause**: Scope mismatch or unverified app

- Check API enablement in service console
- Verify OAuth scopes match API operations
- Add test users if app is unverified
- Re-authorize after scope changes

### Redirect URI Mismatch

**Root cause**: Exact string mismatch

- Protocol (https vs http)
- Domain casing
- Trailing slashes
- Plugin ID accuracy

### No Refresh Token

**Root cause**: Missing offline access request

```python
# Wrong
params = {"scope": "user:email"}

# Right  
params = {
    "scope": "user:email",
    "access_type": "offline",
    "prompt": "consent"
}
```

### Token Refresh Fails

**Root cause**: Scope changes invalidate refresh tokens

- Users must re-authorize completely
- Refresh tokens can expire (Google: 6 months inactive)
- Some services don't provide refresh tokens

## Production Considerations

**Rate Limits**: Implement exponential backoff for API calls
**Error Handling**: Graceful degradation when tokens expire
**Scope Minimization**: Request only necessary permissions
**Security**: Never log access tokens
**User Communication**: Clear error messages for re-authorization

**Testing Strategy**:

1. Test with multiple user accounts
2. Test token expiry scenarios
3. Test scope changes requiring re-auth
4. Test Self-Hosted vs SaaS deployment modes

The biggest mistake developers make is not understanding the deployment architecture upfront. Choose your target deployment model first, then implement accordingly.