export default function uniqueBy (arr, fn) {
  const identifiers = new Set()
  return arr.filter(function (item) {
    const identifier = fn(item)

    if (!identifiers.has(identifier)) {
      identifiers.add(identifier)
      return true
    }
  })
}
