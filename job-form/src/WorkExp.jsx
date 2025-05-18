import React from 'react'

export const WorkExp = ({ setPage, formData, setFormData }) => {
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
                <h1 className={titleClasses}>Experience and Skills</h1>
                <div>
                    <label htmlFor="education" className={inputLabelClasses}>Education</label>
                    <textarea
                        id="education"
                        name="education"
                        value={formData.education}
                        onChange={handleChange}
                        className={textareaClasses}
                    />
                </div>
                <div>
                    <label htmlFor="experience" className={inputLabelClasses}>Experience</label>
                    <textarea
                        id="experience"
                        name="experience"
                        value={formData.experience}
                        onChange={handleChange}
                        className={textareaClasses}
                    />
                </div>
                <div>
                    <label htmlFor="skills" className={inputLabelClasses}>Skills</label>
                    <textarea
                        id="skills"
                        name="skills"
                        value={formData.skills}
                        onChange={handleChange}
                        className={textareaClasses}
                    />
                </div>
                <div className="flex justify-between">
                    <button onClick={() => {
                        setPage('Profile')
                    }} className={buttonClasses}>Previous</button>
                    <button type='submit' className={buttonClasses}>Submit</button>
                </div>
            </div>
        </div>
    );
}
