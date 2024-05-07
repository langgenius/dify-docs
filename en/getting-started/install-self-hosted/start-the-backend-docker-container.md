# Start the server Docker container separately

When doing front-end development, if you do not need to build and start the back-end code locally, you can use `docker-compose.yml` to start the back-end service separately. Here are the specific steps:

### Build Docker image using source code

1. Remove the `web` service in `docker-compose.yml`:
   This step ensures that the front-end service is not started.

2. **(Optional) Expose `api` service port `5001`**:
   If you need to access the backend service directly, you can choose to expose the required port.

3. **Start the backend service**:
   Use the following command to start the Docker container:

    ```shell
    docker compose up -d
    ```

4. **Start the front-end service**:
   - If you performed step 2 and exposed the port, you can start the front-end service directly:

     ```shell
     cd web && yarn && yarn dev
     ```

   - If there are no exposed ports, you need to set the environment variables `CONSOLE_URL` and `APP_URL` when starting the frontend. This usually depends on the Nginx configuration. For example:

     ```shell
     CONSOLE_URL=http://localhost APP_URL=http://localhost yarn dev
     ```

     Or by configuring the `.env` file:
     ```
      NEXT_PUBLIC_API_PREFIX=http://localhost/console/api
      NEXT_PUBLIC_PUBLIC_API_PREFIX=http://localhost/api
     ```


     > Note: 80 is the default port. If you use the default port, you can omit it during configuration.

     ![Nginx configuration](../../../zh_CN/.gitbook/assets/nginx-config.png)

### Local access

Visit [http://localhost:3000](http://localhost:3000) to view the front-end application.