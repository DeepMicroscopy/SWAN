import createClient from 'openapi-fetch';
import type { paths } from '@/api.v1.ts';

function getCookie (name: string) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  return parts.length === 2 ? parts.pop()?.split(';').shift() : null;
}

const token = getCookie('csrftoken')
const client = createClient<paths>({
  headers: {
    'X-CSRFToken': token,
  },
})

export default client
