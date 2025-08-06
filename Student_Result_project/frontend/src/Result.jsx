import { use, useEffect, useState } from "react";

export default function Result() {
    useEffect(() => {}, []);

    return (
        <div className="dark:text-white dark:bg-[#1a1a1a] text-black w-[80vw] h-[70vh] flex justify-center backdrop-blur-sm items-center border-4 border-black">
            <h1>Result</h1>
        </div>
    );
}
