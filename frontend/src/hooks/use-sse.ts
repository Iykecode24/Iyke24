import { useEffect, useState } from 'react';

export const useSSE = (url: string) => {
  const [data, setData] = useState<any>(null);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const eventSource = new EventSource(url);

    eventSource.onmessage = (event) => {
      try {
        setData(JSON.parse(event.data));
      } catch (err) {
        setData(event.data);
      }
    };

    eventSource.onerror = (err) => {
      setError(err as any);
      eventSource.close();
    };

    return () => {
      eventSource.close();
    };
  }, [url]);

  return { data, error };
};
