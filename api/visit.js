// POST /api/visit: the site calls this once per browser tab. Stores referrer, timezone, device
// and the coarse place Vercel derives from the request (country and city). No IP, no cookies.
const { cmd, ready } = require('./_kv')

const clean = (s, n) => String(s || '').replace(/[|\n\r]/g, ' ').slice(0, n)

module.exports = async (req, res) => {
  res.setHeader('Cache-Control', 'no-store')
  if (req.method !== 'POST') return res.status(405).end()
  if (!ready()) return res.status(204).end()
  try {
    const b = typeof req.body === 'string' ? JSON.parse(req.body || '{}') : req.body || {}
    const city = decodeURIComponent(req.headers['x-vercel-ip-city'] || '')
    const visit = {
      id: Date.now().toString(36) + Math.random().toString(36).slice(2, 6),
      t: Date.now(),
      from: clean(b.from, 60),
      tz: clean(b.tz, 40),
      device: b.device === 'phone' ? 'phone' : 'desktop',
      country: clean(req.headers['x-vercel-ip-country'], 2),
      city: clean(city, 40),
    }
    await cmd('LPUSH', 'cv:visits', JSON.stringify(visit))
    await cmd('LTRIM', 'cv:visits', 0, 499)
  } catch (e) {}
  res.status(204).end()
}
