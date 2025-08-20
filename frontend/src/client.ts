import createClient, { type Middleware } from 'openapi-fetch';
import type { paths } from '@/api.v1.ts';

function getCookie (name: string): string {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);

  if (parts.length === 2) {
    return parts.pop()!.split(';').shift()!;
  } else {
    return 'n/a'
  }
}

const csrfMiddleware: Middleware = {
  async onRequest ({ request }) {
    request.headers.set('X-CSRFToken', getCookie('csrftoken'));
    return request;
  },
};

const client = createClient<paths>()

client.use(csrfMiddleware);

export default client
