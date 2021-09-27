export default function debounce (fn) {
  let pending
  return function () {
    if (!pending) {
      pending = new Promise(function (resolve) {
        Promise.resolve().then(function () {
          pending = undefined
          resolve(fn())
        })
      })
    }

    return pending
  }
}
