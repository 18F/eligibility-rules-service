import fetch from 'cross-fetch';
import htmlescape from 'htmlescape';
import 'cross-fetch/polyfill';

const apiUrl = process.env.GATSBY_API_URL;

const post = (payload) => {
  return fetch(apiUrl, {
    method: 'POST',
    body: htmlescape(payload),
    headers: {
      'Content-Type': 'application/json',
    },
  }).then((res) => {
    if (res.status >= 400) {
      return {
        message: 'Bad response from server',
        error: res,
      };
    }
    return res.json();
  });
};

export default post;
