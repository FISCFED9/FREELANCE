const CHATWOOT_SCRIPT_ID = "chatwoot-sdk";

export function initChatwoot() {
  const baseUrl = import.meta.env.VITE_CHATWOOT_BASE_URL;
  const websiteToken = import.meta.env.VITE_CHATWOOT_WEBSITE_TOKEN;

  if (!baseUrl || !websiteToken) return;
  if (document.getElementById(CHATWOOT_SCRIPT_ID)) return;

  window.chatwootSettings = { hideMessageBubble: false, position: "right" };

  const script = document.createElement("script");
  script.id = CHATWOOT_SCRIPT_ID;
  script.src = `${baseUrl}/packs/js/sdk.js`;
  script.async = true;
  script.onload = () => {
    if (window.chatwootSDK) {
      window.chatwootSDK.run({
        websiteToken,
        baseUrl,
      });
    }
  };
  document.body.appendChild(script);
}
