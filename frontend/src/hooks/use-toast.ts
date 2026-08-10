import { useNotificationStore } from '@/stores/notification-store';

export const useToast = () => {
  const { toasts, addToast, removeToast } = useNotificationStore();

  const toast = {
    success: (msg: string) => addToast(msg, 'success'),
    error: (msg: string) => addToast(msg, 'error'),
    warning: (msg: string) => addToast(msg, 'warning'),
    info: (msg: string) => addToast(msg, 'info'),
  };

  return { toasts, toast, removeToast };
};
