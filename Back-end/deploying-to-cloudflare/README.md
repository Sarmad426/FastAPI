# Deploying API to Cloudflare

Cloudflare offers a tunneling service that allows you to expose your local server to the internet. This is useful for testing your API on a live server before deploying it to a production server.

Let's deploy our API to Cloudflare using the tunneling service.

## 1. Install Cloudflare CLI (windows)

```bash
winget install --id Cloudflare.cloudflared
```

For other OS checkout these docs: <https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/#github-repository>

## 2. Run FastAPI api in a terminal

```bash
uvicorn main:app --reload
```

## 3. Run Cloudflare tunnel

Open another terminal and run the following command:

```bash
cloudflared tunnel --url http://127.0.0.1:8000
```

**Note:**

This example is not only specific for FastAPI. Update the `--url` parameter with the URL of your server to deploy the API you want.

After running this command you will receive a url that you can use to access your API from anywhere in the world.

It is important to note that the URL will be different every time you run the command. Also it is temporary and will no longer be available after you stop the tunnel.

For more details: <https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/do-more-with-tunnels/trycloudflare/>
