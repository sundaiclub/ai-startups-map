"use client";
import React from "react";

const HeroSection: React.FC = () => {
  const handleButtonClick = () => {
    document.getElementById("app")?.scrollIntoView({ behavior: "smooth" });
  };

  return (
    <section className="flex h-screen w-full flex-col items-center justify-center bg-gray-100 lg:flex-row">
      <div className="relative h-full w-full lg:w-1/2">
        <video
          src="1.mp4" // Replace this with the actual path to your video
          autoPlay
          loop
          muted
          className="h-full w-full object-cover"
        />
        <div className="absolute left-10 top-10 text-2xl font-bold text-white">
          travel.sundai.club
        </div>
      </div>

      {/* Right Side - Text Content */}
      <div className="relative flex h-full w-full flex-col items-center justify-center p-8 text-center lg:w-1/2">
        {/* Top Sliding Text */}
        <div className="absolute top-0 w-full overflow-hidden">
          <div className="animate-slide-left whitespace-nowrap text-xl font-semibold text-gray-800">
            travel buddy travel buddy travel buddy travel buddy travel buddy
            travel buddy travel buddy
          </div>
        </div>

        <h2 className="mb-4 mt-8 text-4xl font-bold text-gray-800 lg:text-6xl">
          Eager to take off?
        </h2>
        <p className="mb-4 text-lg text-gray-600">start planning now with</p>
        <h1 className="text-5xl font-extrabold text-red-500 lg:text-7xl">
          Travel Buddy
        </h1>

        {/* Elegant Button */}
        <button
          onClick={handleButtonClick}
          className="mt-8 rounded-full border-2 border-red-500 bg-white px-6 py-3 text-lg font-bold text-red-500 transition duration-300 ease-in-out hover:bg-gradient-to-r hover:from-red-500 hover:to-orange-500 hover:text-white focus:outline-none focus:ring-4 focus:ring-red-300"
        >
          Start Your Journey
        </button>

        {/* Bottom Rolling Text */}
        <div className="absolute bottom-0 w-full overflow-hidden">
          <div className="animate-slide-right whitespace-nowrap text-xl font-semibold text-gray-800">
            travel smarter travel smarter travel smarter travel smarter travel
            smarter travel smarter travel smarter
          </div>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;
