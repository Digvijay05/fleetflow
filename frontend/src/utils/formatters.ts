/**
 * Indian locale formatting utilities.
 */

/** Format a number as Indian Rupees (₹). */
export const formatINR = (amount: number): string => {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR',
        maximumFractionDigits: 0,
    }).format(amount);
};

/** Format a number with Indian comma grouping (e.g., 1,25,000). */
export const formatIndianNumber = (num: number): string => {
    return new Intl.NumberFormat('en-IN').format(num);
};

/** Format an ISO date string as DD/MM/YYYY. */
export const formatDateIN = (dateString: string | null | undefined): string => {
    if (!dateString) return '—';
    return new Date(dateString).toLocaleDateString('en-IN', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
    });
};

/** Format an ISO datetime string as DD/MM/YYYY HH:MM. */
export const formatDateTimeIN = (dateString: string | null | undefined): string => {
    if (!dateString) return '—';
    const d = new Date(dateString);
    return d.toLocaleDateString('en-IN', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
    }) + ' ' + d.toLocaleTimeString('en-IN', {
        hour: '2-digit',
        minute: '2-digit',
        hour12: false,
    });
};
