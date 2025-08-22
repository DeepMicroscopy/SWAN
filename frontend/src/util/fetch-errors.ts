export interface ErrorDetail {
  detail: string
}

export interface ErrorData {
  show: boolean;
  text: string;
  code?: number
}

export function getError (): ErrorData {
  return {
    show: false,
    text: '',
  }
}

export function setError (error: ErrorData, result: unknown, response: Response) {
  const err = result as ErrorDetail

  error.show = true
  error.text = err.detail ?? 'Unknown error'
  error.code = response.status
}
