export default {
  install(app) {
    const icons = import.meta.globEager('@/components/icons/*.vue')

    Object.keys(icons).forEach((key) => {
      const iconComponent = icons[key].default
      app.component(iconComponent.name, iconComponent)
    })
  }
}
