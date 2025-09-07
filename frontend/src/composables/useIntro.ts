import { type Driver, driver, type DriveStep, type Popover } from 'driver.js';

export type IntroStep = {
  ref: string
  onEnter?: () => void
  onExit?: () => void
} & Popover

export function useIntro (steps: IntroStep[]): Driver {
  const intro = driver(
    {
      showProgress: true,
      stagePadding: 5,
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
            ...step,
            onPopoverRender: () =>{
              if (step.onEnter) {
                step.onEnter()
              }
            },
            onNextClick: () => {
              intro.moveNext()

              if (step.onExit) {
                step.onExit()
              }
            },
            onPrevClick: () => {
              intro.movePrevious()

              if (step.onExit) {
                step.onExit()
              }
            },
            onCloseClick: () => {
              intro.destroy()

              if (step.onExit) {
                step.onExit()
              }
            },
          },
        } as DriveStep
      })
    )

    intro.drive()

  })
  return intro
}
