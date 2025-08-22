# Overview

## Components

Vue template files in this folder are automatically imported.

### Usage

Importing is handled by [unplugin-vue-components](https://github.com/unplugin/unplugin-vue-components). This plugin automatically imports `.vue` files created in the `src/components` directory, and registers them as global components. This means that you can use any component in your application without having to manually import it.

The following example assumes a component located at `src/components/MyComponent.vue`:

```vue
<template>
  <div>
    <MyComponent />
  </div>
</template>

<script lang="ts" setup>
  //
</script>
```

When your template is rendered, the component's import will automatically be inlined, which renders to this:

```vue
<template>
  <div>
    <MyComponent />
  </div>
</template>

<script lang="ts" setup>
  import MyComponent from '@/components/MyComponent.vue'
</script>
```


## Layouts

Layouts are reusable components that wrap around pages. They are used to provide a consistent look and feel across multiple pages.

Full documentation for this feature can be found in the Official [vite-plugin-vue-layouts-next](https://github.com/loicduong/vite-plugin-vue-layouts-next) repository.


## Pages

Vue components created in this folder will automatically be converted to navigatable routes.

Full documentation for this feature can be found in the Official [unplugin-vue-router](https://github.com/posva/unplugin-vue-router) repository.


## Store

Pinia stores are used to store reactive state and expose actions to mutate it.

Full documentation for this feature can be found in the Official [Pinia](https://pinia.esm.dev/) repository.