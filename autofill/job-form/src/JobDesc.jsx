import React from 'react'

export const JobDesc = ({ setPage }) => {
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
                <header>
                    <h1 className={titleClasses}>
                        Internship, Robotics Modeling, Optimus (Fall 2025)
                    </h1>
                    <div className="flex flex-wrap gap-2">
                        <span className={badgeClasses}>
                            AI & Robotics
                        </span>
                        <span className={badgeClasses}>
                            Palo Alto, CA
                        </span>
                        <span className={badgeClasses}>
                            Intern/Apprentice
                        </span>
                    </div>
                </header>
                <main className="space-y-6">
                    <section>
                        <h2 className={sectionTitleClasses}>
                            Job Description
                        </h2>
                        <div className={descriptionTextClasses}>
                            We are seeking a motivated and talented Robotics Modeling Intern to join our team in Palo Alto for the Fall 2025 term.  This internship will provide hands-on experience in developing and refining models for our Optimus humanoid robot.  You will work alongside experienced engineers and researchers to contribute to the cutting-edge of robotics.
                            <br /><br />
                            Responsibilities may include:
                            <ul className="list-disc list-inside mt-2 space-y-1">
                                <li className={listItemClasses}>Developing and maintaining simulation models of robot systems.</li>
                                <li className={listItemClasses}>Designing and implementing new modeling techniques.</li>
                                <li className={listItemClasses}>Analyzing simulation data to improve model accuracy.</li>
                                <li className={listItemClasses}>Collaborating with hardware and software teams.</li>
                                <li className={listItemClasses}>Contributing to research and development efforts.</li>
                            </ul>
                        </div>
                    </section>

                    <section>
                        <h2 className={sectionTitleClasses}>
                            Qualifications
                        </h2>
                        <ul className="list-disc list-inside mt-2 space-y-2">
                            <li className={listItemClasses}>Currently pursuing a Bachelor's or Master's degree in Robotics, Mechanical Engineering, Computer Science, or a related field.</li>
                            <li className={listItemClasses}>Strong understanding of robotics principles, including kinematics, dynamics, and control.</li>
                            <li className={listItemClasses}>Experience with simulation software (e.g., Gazebo, MuJoCo, Simscape) is a plus.</li>
                            <li className={listItemClasses}>Proficiency in programming languages such as Python or C++.</li>
                            <li className={listItemClasses}>Excellent problem-solving and communication skills.</li>
                        </ul>
                    </section>

                    <button
                        onClick={() => {
                            setPage('Profile')
                        }}
                        className={applyButtonClasses}
                    >
                        Apply Now
                    </button>
                </main>
            </div>
        </div>
    );
}