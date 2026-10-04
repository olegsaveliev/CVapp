// Tiny Upstash Redis REST helper (the Vercel "Upstash for Redis" integration sets these env vars).
const URL_ = process.env.KV_REST_API_URL || process.env.UPSTASH_REDIS_REST_URL
const TOKEN = process.env.KV_REST_API_TOKEN || process.env.UPSTASH_REDIS_REST_TOKEN

async function cmd(...args) {
  const r = await fetch(URL_, {
    method: 'POST',
    headers: { Authorization: `Bearer ${TOKEN}`, 'Content-Type': 'application/json' },
    body: JSON.stringify(args),
  })
  if (!r.ok) throw new Error(`kv ${r.status}`)
  return (await r.json()).result
}

module.exports = { cmd, ready: () => Boolean(URL_ && TOKEN) }
