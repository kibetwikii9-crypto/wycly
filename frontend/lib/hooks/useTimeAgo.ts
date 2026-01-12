'use client';

import { useState, useEffect } from 'react';

/**
 * Hook that returns a formatted "time ago" string that updates in real-time
 * Updates every second for recent times, less frequently for older times
 */
export function useTimeAgo(timestamp: string | null | undefined): string {
  const [timeAgo, setTimeAgo] = useState<string>('');

  useEffect(() => {
    if (!timestamp) {
      setTimeAgo('Unknown');
      return;
    }

    const formatTime = () => {
      const date = new Date(timestamp);
      const now = new Date();
      const diffMs = now.getTime() - date.getTime();
      
      // Handle future dates
      if (diffMs < 0) {
        setTimeAgo('Just now');
        return;
      }

      const diffSeconds = Math.floor(diffMs / 1000);
      const diffMins = Math.floor(diffMs / 60000);
      const diffHours = Math.floor(diffMs / 3600000);
      const diffDays = Math.floor(diffMs / 86400000);
      const diffWeeks = Math.floor(diffMs / 604800000);
      const diffMonths = Math.floor(diffMs / 2592000000);
      const diffYears = Math.floor(diffMs / 31536000000);

      if (diffSeconds < 10) {
        setTimeAgo('Just now');
      } else if (diffSeconds < 60) {
        setTimeAgo(`${diffSeconds}s ago`);
      } else if (diffMins < 60) {
        setTimeAgo(`${diffMins}m ago`);
      } else if (diffHours < 24) {
        setTimeAgo(`${diffHours}h ago`);
      } else if (diffDays < 7) {
        setTimeAgo(`${diffDays}d ago`);
      } else if (diffWeeks < 4) {
        setTimeAgo(`${diffWeeks}w ago`);
      } else if (diffMonths < 12) {
        setTimeAgo(`${diffMonths}mo ago`);
      } else {
        setTimeAgo(`${diffYears}y ago`);
      }
    };

    // Format immediately
    formatTime();

    // Determine update interval based on age
    const diffMs = new Date().getTime() - new Date(timestamp).getTime();
    let interval: number;
    
    if (diffMs < 60000) {
      // Less than 1 minute: update every second
      interval = 1000;
    } else if (diffMs < 3600000) {
      // Less than 1 hour: update every 10 seconds
      interval = 10000;
    } else if (diffMs < 86400000) {
      // Less than 1 day: update every minute
      interval = 60000;
    } else {
      // Older: update every 5 minutes
      interval = 300000;
    }

    const timer = setInterval(formatTime, interval);

    return () => clearInterval(timer);
  }, [timestamp]);

  return timeAgo;
}

