import React from 'react'

export const Profile = ({ setPage, formData, setFormData }) => {
    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    const containerClasses = "flex items-center justify-center min-h-screen bg-gray-100 dark:bg-gray-900 p-4";
    const cardClasses = "w-full max-w-2xl bg-white dark:bg-gray-800 shadow-lg border border-gray-200 dark:border-gray-700 rounded-xl p-6 space-y-6";
    const titleClasses = "text-2xl font-semibold text-gray-900 dark:text-white mb-4";
    const badgeClasses = "bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200 border border-gray-200 dark:border-gray-600 px-2 py-1 rounded-full text-sm";
    const applyButtonClasses = "w-full bg-blue-500 hover:bg-blue-600 text-white font-semibold py-3 rounded-md transition-colors duration-200 text-center cursor-pointer";
    const descriptionTextClasses = "text-gray-700 dark:text-gray-300 leading-relaxed";
    const sectionTitleClasses = "text-xl font-semibold text-gray-900 dark:text-white mb-3";
    const listItemClasses = "text-gray-700 dark:text-gray-300";
    const inputLabelClasses = "block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1";
    const inputClasses = "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500";
    const textareaClasses = "mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 min-h-[100px]";
    const buttonClasses = "bg-blue-500 hover:bg-blue-600 text-white font-semibold py-3 px-6 rounded-md transition-colors duration-200 cursor-pointer";

    return (
        <div className={containerClasses}>
            <div className={cardClasses}>
                <h1 className={titleClasses}>Personal Information</h1>
                <div className="grid grid-cols-2 gap-4">
                    <div>
                        <label htmlFor="firstName" className={inputLabelClasses}>First Name</label>
                        <input
                            type="text"
                            id="firstName"
                            name="firstName"
                            value={formData.firstName}
                            onChange={handleChange}
                            className={inputClasses}
                        />
                    </div>
                    <div>
                        <label htmlFor="lastName" className={inputLabelClasses}>Last Name</label>
                        <input
                            type="text"
                            id="lastName"
                            name="lastName"
                            value={formData.lastName}
                            onChange={handleChange}
                            className={inputClasses}
                        />
                    </div>
                    <div>
                        <label htmlFor="middleName" className={inputLabelClasses}>Middle Name (Optional)</label>
                        <input
                            type="text"
                            id="middleName"
                            name="middleName"
                            value={formData.middleName}
                            onChange={handleChange}
                            className={inputClasses}
                        />
                    </div>
                    <div>
                        <label htmlFor="preferredName" className={inputLabelClasses}>Preferred Name (Optional)</label>
                        <input
                            type="text"
                            id="preferredName"
                            name="preferredName"
                            value={formData.preferredName}
                            onChange={handleChange}
                            className={inputClasses}
                        />
                    </div>
                    <div>
                        <label htmlFor="phone" className={inputLabelClasses}>Phone</label>
                        <input
                            type="tel"
                            id="phone"
                            name="phone"
                            value={formData.phone}
                            onChange={handleChange}
                            className={inputClasses}
                        />
                    </div>
                    <div>
                        <label htmlFor="phoneType" className={inputLabelClasses}>Phone Type</label>
                        <select
                            id="phoneType"
                            name="phoneType"
                            value={formData.phoneType}
                            onChange={handleChange}
                            className={inputClasses}
                        >
                            <option value="">- Select type -</option>
                            <option value="Home">Home</option>
                            <option value="Mobile">Mobile</option>
                        </select>

                    </div>
                    <div>
                        <label htmlFor="email" className={inputLabelClasses}>Email</label>
                        <input
                            type="text"
                            id="email"
                            name="email"
                            value={formData.email}
                            onChange={handleChange}
                            className={inputClasses}
                        />
                    </div>
                    <div>
                        <label htmlFor="country" className={inputLabelClasses}>Country</label>
                        <input
                            type="text"
                            id="country"
                            name="country"
                            value={formData.country}
                            onChange={handleChange}
                            className={inputClasses}
                        />
                    </div>
                </div>
                <div className="flex justify-end">
                    <button onClick={() => {
                        setPage('WorkExp')
                    }} className={buttonClasses}>Next</button>
                </div>
            </div>
        </div>
    );
}
