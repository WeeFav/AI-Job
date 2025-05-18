import React, { useState } from 'react';
import { JobDesc } from './JobDesc';
import { Profile } from './Profile';
import { WorkExp } from './WorkExp';
import { Done } from './Done';

const JobApplicationForm = () => {
    const [page, setPage] = useState("JobDesc");
    const [formData, setFormData] = useState({
        firstName: '',
        lastName: '',
        middleName: '',
        preferredName: '',
        phone: '',
        phoneType: '',
        email: '',
        country: '',
        startDate: ''
    });

    const renderPage = () => {
        switch (page) {
            case "JobDesc":
                return <JobDesc setPage={setPage} />

            case "Profile":
                return <Profile setPage={setPage} formData={formData} setFormData={setFormData} />

            case "WorkExp":
                return <WorkExp setPage={setPage} formData={formData} setFormData={setFormData} />

            case "Done":
                return <Done />

            default:
                return <div>Error: Invalid page number.</div>;
        }
    };

    return (
        <form onSubmit={(e) => {
            e.preventDefault()
            setPage('Done')
        }}>
            <div>
                {renderPage()}
            </div>
        </form>
    );
};

export default JobApplicationForm;
