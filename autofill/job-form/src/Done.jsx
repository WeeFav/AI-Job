import React from 'react'

export const Done = () => {
    const containerClasses = "flex items-center justify-center min-h-screen bg-gray-100 dark:bg-gray-900 p-4";
    const cardClasses = "w-full max-w-2xl bg-white dark:bg-gray-800 shadow-lg border border-gray-200 dark:border-gray-700 rounded-xl p-6 space-y-6";
    const titleClasses = "text-2xl font-semibold text-gray-900 dark:text-white mb-4";

    return (
        <div className={containerClasses}>
            <div className={cardClasses}>
                <h1 className={titleClasses}>Thank you for applying</h1>
            </div>
        </div>
    );

}
