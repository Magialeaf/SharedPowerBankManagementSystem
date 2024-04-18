import { $errorMsg } from '@/utils/msg'

export function lockFunction(lockDurationMs = 3000) {
  let lastUnlockTime = 0

  return function wrapWithLock(fn) {
    return function (...args) {
      const now = Date.now()
      const timeSinceLastUnlock = now - lastUnlockTime

      if (timeSinceLastUnlock < lockDurationMs) {
        const second = parseInt((lockDurationMs - timeSinceLastUnlock) / 1000)
        $errorMsg(`操作太频繁了，请等待${second} s`)
        return
      }

      lastUnlockTime = now
      return fn.apply(this, args)
    }
  }
}
