---
sidebar_position: 1
sidebar_label: Configuration
description: Configure OAuth 2.0 and asynchronous events
---

# Configuration

Follow this guide in order to:

1. Enable AutoKitteh connections to use OAuth 2.0, instead of
   GCP service account JSON keys
2. Enable asynchronous events from Gmail and Google Forms

:::note

This guide assumes that the AutoKitteh server is already configured with
[HTTP tunneling](/config/http_tunneling).

:::

## Google Cloud Platform (GCP) Project

1. Create a new GCP project

   - Follow the instructions at:
     https://developers.google.com/workspace/guides/create-project
   - Quick link: https://console.cloud.google.com/projectcreate

2. Enable Google Workspace APIs in it

   - Follow the instructions at:
     https://developers.google.com/workspace/guides/enable-apis
   - Quick links
     - Calendar:
       https://console.cloud.google.com/apis/enableflow?apiid=calendar-json.googleapis.com
     - Chat:
       https://console.cloud.google.com/apis/enableflow?apiid=chat.googleapis.com
     - Cloud Pub/Sub:
       https://console.cloud.google.com/apis/library/pubsub.googleapis.com
     - Docs:
       https://console.cloud.google.com/apis/enableflow?apiid=docs.googleapis.com
     - Drive:
       https://console.cloud.google.com/apis/enableflow?apiid=drive.googleapis.com
     - Forms:
       https://console.cloud.google.com/apis/enableflow?apiid=forms.googleapis.com
     - Gmail:
       https://console.cloud.google.com/apis/enableflow?apiid=gmail.googleapis.com
     - Sheets:
       https://console.cloud.google.com/apis/enableflow?apiid=sheets.googleapis.com

## OAuth Consent Screen

1. Create an OAuth consent screen for your GCP project

   - Follow the instructions at:
     https://developers.google.com/workspace/guides/configure-oauth-consent
   - Quick link: https://console.cloud.google.com/apis/credentials/consent

2. Specify authorized domains for it

   - The AutoKitteh server's [public tunnel address](/config/http_tunneling)
     (just the address, no `https://` prefix, and no path suffix)

3. Add these permission scopes to it

   - Non-sensitive:
     - `.../auth/userinfo.email`
     - `.../auth/userinfo.profile`
     - `openid`
   - Sensitive:
     - `.../auth/calendar`
     - `.../auth/calendar.events`
     - `.../auth/chat.memberships`
     - `.../auth/chat.messages`
     - `.../auth/chat.spaces`
     - `.../auth/forms.body`
     - `.../auth/forms.responses.readonly`
     - `.../auth/spreadsheets`
   - Restricted:
     - `.../auth/drive`
     - `.../auth/gmail.modify`
     - `.../auth/gmail.settings.basic`

## Credentials

1. Create an OAuth 2.0 Client ID

   - Follow the instructions at:
     https://developers.google.com/workspace/guides/create-credentials#oauth-client-id
   - Quick link: https://console.cloud.google.com/apis/credentials

2. Specific steps and settings

   - Click: `+ Create Credentials`
   - Select: `OAuth client ID`
   - Application type: `Web application`
   - Authorized redirect URI:
     - `https://PUBLIC-AK-ADDRESS/oauth/redirect/google`
     - (`PUBLIC-AK-ADDRESS` is the AutoKitteh server's
       [public tunnel address](/config/http_tunneling))

## Cloud Pub/Sub

This is required if you wish to receive asynchronous events from Gmail and
Google Forms.

1. Go to your GCP project's service accounts page:
   https://console.cloud.google.com/iam-admin/serviceaccounts

2. Click the `CREATE SERVICE ACCOUNT` button at the top of the page

   <img
   src={require('/img/google/sa1.png').default}
   alt="Screenshot 1: Create service account - button"
   width="373" height="32" border="1" style={{padding: '3px'}} />
   <br/>
   <br/>

   - **Required:** Service account name
   - **Optional:** Service account ID & description
   - Click the `CREATE AND CONTINUE` button

   <br/>
   <img
   src={require('/img/google/sa2.png').default}
   alt="Screenshot 2: Create service account - details"
   width="514" height="341" border="1" style={{padding: '3px'}} />

3. Grant these roles, and click the `CONTINUE` button

   - `Service Account Token Creator`

   <br/>
   <img
   src={require('/img/google/sa3.png').default}
   alt="Screenshot 3: Create service account - roles"
   width="500" height="353" border="1" style={{padding: '3px'}} />

4. Click the `DONE` button (no need to grant user access)

   <img
   src={require('/img/google/sa4.png').default}
   alt="Screenshot 4: Create service account - users"
   width="518" height="303" border="1" style={{padding: '3px'}} />

5. Go to your GCP project's Cloud Pub/Sub page:
   https://console.cloud.google.com/cloudpubsub/topic/list

6. Click the `CREATE TOPIC` button at the top of the page

   <img
   src={require('/img/google/ps1.png').default}
   alt="Screenshot 4: Create topic - button"
   width="220" height="36" border="1" style={{padding: '3px'}} />
   <br/>
   <br/>

   - Topic ID: `forms-notifications`
   - Add a default subscription: **Yes** (default)
   - Enable message retention: **0 Days, 0 Hours, 10 minutes**
   - Click the `CREATE` button

   <br/>
   <img
   src={require('/img/google/ps2.png').default}
   alt="Screenshot 5: Create topic - settings"
   width="520" height="533" border="1" style={{padding: '3px'}} />

7. Permissions: click the `ADD PRINCIPAL` button

   <img
   src={require('/img/google/ps3.png').default}
   alt="Screenshot 6: Add principal - 1"
   width="413" height="333" border="1" style={{padding: '3px'}} />
   <br/>
   <br/>

   - New principal: `forms-notifications@system.gserviceaccount.com`
   - Role: `Pub/Sub Publisher`
   - Click the `SAVE` button

   <br/>
   <img
   src={require('/img/google/ps4.png').default}
   alt="Screenshot 7: Add principal - 2"
   width="516" height="674" border="1" style={{padding: '3px'}} />

8. Click the auto-created subscription `forms-notifications-sub`, and then
   click its `EDIT` button

9. Modify the following details:

   - Delivery type: **Push**
   - Endpoint URL: `https://PUBLIC-AK-ADDRESS/googleforms/notif`
     (`PUBLIC-AK-ADDRESS` is the AutoKitteh server's
     [public tunnel address](/config/http_tunneling))
   - Enable authentication: **Yes**

     - Select the service account you created in step 2 above

   - Enable payload unwrapping: **Yes**

     - Write metadata: **Yes**

     <br/>
     <img
     src={require('/img/google/ps5.png').default}
     alt="Screenshot 8: Edit subscription - 1"
     width="516" height="362" border="1" style={{padding: '3px'}} />

   - Message retention duration: **0 Days, 0 Hours, 10 minutes**

     <img
     src={require('/img/google/ps6.png').default}
     alt="Screenshot 9: Edit subscription - 2"
     width="516" height="177" border="1" style={{padding: '3px'}} />

   - Expiration period: **Never expire**

     <img
     src={require('/img/google/ps7.png').default}
     alt="Screenshot 10: Edit subscription - 3"
     width="509" height="135" border="1" style={{padding: '3px'}} />

   - Acknowledgement deadline: **10** seconds (default)
   - Message ordering: **No** (default)
   - Dead lettering: **No** (default)
   - Retry policy: **Retry immediately** (default)
   - Click the `UPDATE` button

10. Repeat steps 5-9 with these changes:

    - Topic ID: `gmail-api-push`
      - Enable message retention: **10 minutes**
    - New principal with the `Pub/Sub Publisher` role:
      `gmail-api-push@system.gserviceaccount.com`
    - Subscription:
      - Endpoint URL: `https://PUBLIC-AK-ADDRESS/gmail/notif`
        (`PUBLIC-AK-ADDRESS` is the AutoKitteh server's
        [public tunnel address](/config/http_tunneling))
    - Everything else should be the same

## Configure AutoKitteh

There are two equivalent options to configure the AutoKitteh server to
interact with your GCP OAuth consent screen - choose the one most suited for
your needs and constraints.

For more details, see the [Configuration Methods](/config/methods) page.

### `config.yaml` File

Stay tuned!

### Environment Variables

Set this environment variable, based on the AutoKitteh server's
[public tunnel address](/config/http_tunneling):

- `WEBHOOK_ADDRESS`
  - Just the address, without the `https://` prefix, and without a path suffix

Also set these environment variables, based on the generated details in the
[credentials](#credentials) you created above:

- `GOOGLE_CLIENT_ID`
- `GOOGLE_CLIENT_SECRET`

Also set these optional environment variables, based on the topic(s) you
configured in the [Cloud Pub/Sub](#cloud-pubsub) section, if you did so:

- `GMAIL_PUBSUB_TOPIC`
- `GOOGLE_FORMS_PUBSUB_TOPIC`

Lastly, restart the AutoKitteh server for these settings to take effect.
