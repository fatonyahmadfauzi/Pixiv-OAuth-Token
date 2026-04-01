/**
 * OAuth PKCE Module
 */
let codeVerifier = "";
let tokenState = { access_token: "", refresh_token: "" };

/**
 * Encodes bytes to base64url format
 */
export function b64Url(bytes) {
  return btoa(String.fromCharCode(...bytes))
    .replace(/\\+/g, "-")
    .replace(/\\//g, "_")
    .replace(/=+$/, "");
}

/**
 * Creates PKCE challenge and verifier
 */
export async function createPkce() {
  const arr = crypto.getRandomValues(new Uint8Array(32));
  codeVerifier = b64Url(arr);
  const digest = await crypto.subtle.digest(
    "SHA-256",
    new TextEncoder().encode(codeVerifier)
  );
  return {
    codeVerifier: codeVerifier,
    codeChallenge: b64Url([...new Uint8Array(digest)]),
  };
}

export function getCodeVerifier() { return codeVerifier; }
export function getTokenState() { return tokenState; }
export function setTokenState(data) { tokenState = data; }

/**
 * Extracts code from pixiv callback URL or plain code string
 */
export function parseCode(input) {
  const value = input.trim();
  if (!value) return "";
  if (value.startsWith("pixiv://"))
    return new URL(value).searchParams.get("code") || "";
  try {
    return new URL(value).searchParams.get("code") || value;
  } catch {
    return value;
  }
}
