import React, { useState } from 'react';

const JobApplicationForm = () => {
    const [page, setPage] = useState("apply");
    const [formData, setFormData] = useState({
        firstName: '',
        lastName: '',
        middleName: '',
        preferredName: '',
        phone: '',
        phoneType: '',
        email: '',
        address: '',
        city: '',
        state: '',
        zip: '',
        education: '',
        experience: '',
        skills: '',
    });

    const clickApply = () => {
        setPage("page1");
    };

    const clickNext = () => {
        setPage("page2");
    };

    const clickPrev = () => {
        setPage("page1");
    };

    const clickSubmit = () => {
        setPage("done");
    };

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    const renderPage = () => {
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

        switch (page) {
            case "apply":
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

                                <div
                                    onClick={clickApply}
                                    className={applyButtonClasses}
                                >
                                    Apply Now
                                </div>
                            </main>
                        </div>
                    </div>
                );

            case "page1":
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
                                        required
                                    >
                                        <option value="">- Select type -</option>
                                        <option value="Home">Home</option>
                                        <option value="Mobile">Mobile</option>
                                    </select>

                                </div>
                                <div>
                                    <label htmlFor="address" className={inputLabelClasses}>Address</label>
                                    <input
                                        type="text"
                                        id="address"
                                        name="address"
                                        value={formData.address}
                                        onChange={handleChange}
                                        className={inputClasses}
                                    />
                                </div>
                                <div>
                                    <label htmlFor="city" className={inputLabelClasses}>City</label>
                                    <input
                                        type="text"
                                        id="city"
                                        name="city"
                                        value={formData.city}
                                        onChange={handleChange}
                                        className={inputClasses}
                                    />
                                </div>
                                <div>
                                    <label htmlFor="state" className={inputLabelClasses}>State</label>
                                    <input
                                        type="text"
                                        id="state"
                                        name="state"
                                        value={formData.state}
                                        onChange={handleChange}
                                        className={inputClasses}
                                    />
                                </div>
                                <div>
                                    <label htmlFor="zip" className={inputLabelClasses}>Zip</label>
                                    <input
                                        type="text"
                                        id="zip"
                                        name="zip"
                                        value={formData.zip}
                                        onChange={handleChange}
                                        className={inputClasses}
                                    />
                                </div>
                            </div>
                            <div className="flex justify-end">
                                <button onClick={clickNext} className={buttonClasses}>Next</button>
                            </div>
                        </div>
                    </div>
                );

            case "page2":
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
                                <button onClick={clickPrev} className={buttonClasses}>Previous</button>
                                <button onClick={clickSubmit} className={buttonClasses}>Submit</button>
                            </div>
                        </div>
                    </div>
                );

            case "done":
                console.log(formData)
                return (
                    <div className={containerClasses}>
                        <div className={cardClasses}>
                            <h1 className={titleClasses}>Thank you for applying</h1>
                        </div>
                    </div>
                );

            default:
                return <div>Error: Invalid page number.</div>;
        }
    };

    return (
        <div>
            {renderPage()}
        </div>
    );
};

export default JobApplicationForm;
