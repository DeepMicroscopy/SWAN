import { driver, type Driver, type DriveStep } from 'driver.js';

export interface IntroStep {
  ref: string
  title: string
  description: string
}

export function useIntro (steps: IntroStep[]): Driver {
  const intro = driver(
    {
      showProgress: true,
      allowClose: false,
    }
  )

  onMounted(() => {
    const instance = getCurrentInstance()
    if (!instance) return

    intro.setSteps(
      steps.map(step => {
        let el: Element | null = null

        const component = instance.refs[step.ref]
        if (component) {
          if (component instanceof HTMLElement) {
            el = component
          } else if (typeof component === 'object' && '$el' in component) {
            el = component.$el as Element
          } else {
            console.error('unknown component used as ref for useIntro')
          }
        } else {
          console.error('failed getting ref from component')
        }

        return {
          element: el,
          popover: {
            title: step.title,
            description: step.description,
          },
        } as DriveStep
      })
    )

    intro.drive()
  })

  return intro
}
