---
sidebar_label: Configuration
description: Create and install an Auth0 connection
---

# Configuration

Follow this guide in order to enable AutoKitteh's Auth0 connections to use
Auth0's OAuth 2.0

:::note

This guide assumes that the AutoKitteh server is already configured with
[HTTP tunneling](/config/http_tunneling).

:::

## Create an Auth0 app

1. Click here to open your [Auth0 dashboard](https://manage.auth0.com/dashboard/).

2. Click the "Create Application" button.

<div class="setup-image-container">
  <img
  src={require('/img/auth0_app/create.png').default}
  alt="Screenshot 1: Create an app"
  className="setup-image" />
</div>

3. Enter a name for the app, select "Regular Web Application" as the application type and click the "Create" button.

<div class="setup-image-container">
  <img
  src={require('/img/auth0_app/create_2.png').default}
  alt="Screenshot 2: Create an app"
  className="setup-image" />
</div>

4. Click the "Credentials" tab. For "Authentication Method", select "Client Secret (Post)". Click "Save".

<div class="setup-image-container">
  <img
  src={require('/img/auth0_app/credentials.png').default}
  alt="Screenshot 3: Credentials"
  className="setup-image" />
</div>

5. Click the "Settings" tab.

6. Take note of the "Client ID","Client Secret" and "Domain" values – you'll need them later to initialize the Auth0 connection.

<div class="setup-image-container">
  <img
  src={require('/img/auth0_app/settings.png').default}
  alt="Screenshot 4: Settings"
  className="setup-image" />
</div>

7. Scroll down to the "Application URIs" section.

8. Add the following URIs to the "Allowed Callback URLs" field:

   - (For cloud) https://api.autokitteh.cloud/oauth/redirect/auth0
   - (For self-hosted) https://\<example.ngrok.dev\>/oauth/redirect/auth0

   <div class="setup-image-container">
     <img
     src={require('/img/auth0_app/allowed_callback_urls.png').default}
     alt="Screenshot 5: Allowed Callback URLs"
     className="setup-image" />
   </div>

:::tip

For information about obtaining the `example.ngrok.dev` URL, see [HTTP tunneling](../../config/http_tunneling).

:::

9. Scroll down to the "ID Token Expiration" section. Set the "Maximum ID Token Lifetime" to 2592000 seconds (30 days).

:::warning

This is a temporary workaround to prevent the ID token from expiring too quickly. We're actively working on a more permanent fix.

:::

    <div class="setup-image-container">
      <img
      src={require('/img/auth0_app/id_token_expiration.png').default}
      alt="Screenshot 9: ID Token Expiration"
      className="setup-image" />
    </div>

10. Scroll down to the "Advanced Settings" section. Expand the section.

11. Click the "Grant Types" tab. Add the "Client Credentials" grant type.

    <div class="setup-image-container">
      <img
      src={require('/img/auth0_app/grant_types.png').default}
      alt="Screenshot 6: Grant Types"
      className="setup-image" />
    </div>

12. Click the "APIs" tab. Authorize the app to use the "Auth0 Management API".

    <div class="setup-image-container">
      <img
      src={require('/img/auth0_app/api_authorization.png').default}
      alt="Screenshot 7: API Authorization"
      className="setup-image" />
    </div>

13. Expand the "Auth0 Management API" section. Select necessary permissions for your use case.

    <div class="setup-image-container">
      <img
      src={require('/img/auth0_app/api_permissions.png').default}
      alt="Screenshot 8: API Permissions"
      className="setup-image" />
    </div>

14. Click the "Update" button.
