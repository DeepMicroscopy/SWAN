<template>
  <v-footer
    app
    height="40"
  >
    <div
      class="text-caption text-disabled"
      style="position: absolute; right: 16px;"
    >
      &copy; 2025 —
      <a
        class="text-decoration-none on-surface"
        href="https://hs-flensburg.de/"
        rel="noopener noreferrer"
        target="_blank"
      >
        HS Flensburg
      </a>
    </div>
  </v-footer>
</template>

<style scoped lang="sass">
  .social-link :deep(.v-icon)
    color: rgba(var(--v-theme-on-background), var(--v-disabled-opacity))
    text-decoration: none
    transition: .2s ease-in-out

    &:hover
      color: rgba(25, 118, 210, 1)
</style>
