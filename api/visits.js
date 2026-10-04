// GET /api/visits?since=<ms>: newest visits first. Needs the VISITS_KEY secret (header "x-key").
const { cmd, ready } = require('./_kv')

module.exports = async (req, res) => {
  res.setHeader('Cache-Control', 'no-store')
  const key = process.env.VISITS_KEY
  if (!key || req.headers['x-key'] !== key) return res.status(401).json({ error: 'unauthorized' })
  if (!ready()) return res.status(503).json({ error: 'storage not connected' })
  try {
    const since = Number(req.query.since) || 0
    const rows = (await cmd('LRANGE', 'cv:visits', 0, 99)).map(s => JSON.parse(s)).filter(v => v.t > since)
    res.status(200).json({ visits: rows })
  } catch (e) {
    res.status(500).json({ error: 'read failed' })
  }
}
