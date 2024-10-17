# FAQs

### 1. Not receiving reset password emails

You need to configure the `Mail` parameters in the `.env` file. For detailed instructions, please refer to ["Environment Variables Explanation: Mail-related configuration"](https://docs.dify.ai/getting-started/install-self-hosted/environments#mail-related-configuration).

After modifying the configuration, run the following commands to restart the service:

```bash
docker compose down
docker compose up -d
```

If you still haven't received the email, please check if the email service is working properly and whether the email has been placed in the trash list.

### 2. How to handle if the workflow is too complex and exceeds the node limit?

In the community edition, you can manually adjust the MAX\_TREE\_DEPTH limit for single branch depth in `web/app/components/workflow/constants.ts.` Our default value is 50, and it's important to note that excessively deep branches may affect performance in self-hosted scenarios.
