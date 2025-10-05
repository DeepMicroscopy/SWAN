import { type Driver, driver, type DriveStep, type Popover } from 'driver.js';

type Step = {
  child: string
  ref: string
  onEnter?: (step: IntroStep) => void
  onPrev?: (step: IntroStep) => void
  onNext?: (step: IntroStep) => void
  onClose?: (step: IntroStep) => void
}

export type IntroStep = Step & Popover

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

        const child = instance.refs[step.child]
        if (!child) {
          throw new Error('child not found')
        }

        const component = (child as never)[step.ref] as object
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
            onPopoverRender: () => {
              if (step.onEnter) {
                step.onEnter(step)
              }
            },
            onNextClick: () => {
              if (step.onNext) {
                step.onNext(step)
              }

              intro.moveNext()
            },
            onPrevClick: () => {
              intro.movePrevious()

              if (step.onPrev) {
                step.onPrev(step)
              }
            },
            onCloseClick: () => {
              intro.destroy()

              if (step.onClose) {
                step.onClose(step)
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
