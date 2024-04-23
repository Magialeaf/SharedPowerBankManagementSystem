// iconsLoader.js
export const icons = import.meta.glob('@/components/icons/*.vue', { eager: true })

const keys = Object.keys(icons)
// 执行批量替换操作
for (let path of keys) {
  // 裁剪字符串方式得到路径中的文件名（无扩展名）
  let name = path.substring(path.lastIndexOf('/') + 1, path.lastIndexOf('.vue'))
  // 对原对象执行添加新的属性并删除旧属性达到处理效果
  icons[name] = icons[path].default
  delete icons[path]
}
