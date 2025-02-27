// EpsteinDriveCalculator v0.1

import React, { useState, useEffect } from 'react';

// Physical constants
const C = 299792458; // Speed of light in m/s
const LY_TO_M = 9.461e15; // Light years to meters
const YEAR_TO_SECONDS = 365.25 * 24 * 3600;

// Define star systems with distances in light years
const STAR_SYSTEMS = [
  { name: "Tau Ceti", distance: 11.9 },
  { name: "Alpha Centauri", distance: 4.37 },
  { name: "Epsilon Eridani", distance: 10.5 },
  { name: "Barnard's Star", distance: 5.96 },
  { name: "Sirius", distance: 8.6 },
  { name: "Proxima Centauri", distance: 4.24 },
  { name: "Wolf 359", distance: 7.86 },
  { name: "Lalande 21185", distance: 8.29 }
];

// Original Nauvoo specifications
const NAUVOO_SPECS = {
  dryMass: 13500000, // kg (13,500 tons)
  thrust: 144e6, // N (144 MN)
  exhaustVelocity: 0.08 * C, // m/s (0.08c)
  efficiency: 0.0065, // 0.65%
  maxVelocity: 0.119 * C, // m/s (11.9% of c)
  star: STAR_SYSTEMS[0] // Tau Ceti
};

const EpsteinDriveCalculator = () => {
  // Ship parameters
  const [dryMass, setDryMass] = useState(NAUVOO_SPECS.dryMass);
  const [thrust, setThrust] = useState(NAUVOO_SPECS.thrust);
  const [exhaustVelocity, setExhaustVelocity] = useState(NAUVOO_SPECS.exhaustVelocity);
  const [efficiency, setEfficiency] = useState(NAUVOO_SPECS.efficiency);
  const [maxVelocity, setMaxVelocity] = useState(NAUVOO_SPECS.maxVelocity);
  const [selectedStar, setSelectedStar] = useState(NAUVOO_SPECS.star);
  
  // Calculated results
  const [results, setResults] = useState(null);

  const formatNumber = (number, decimals = 1) => {
    return number.toLocaleString(undefined, { 
      minimumFractionDigits: decimals,
      maximumFractionDigits: decimals
    });
  };

  const formatPower = (watts) => {
    if (watts >= 1e15) {
      return `${(watts/1e15).toFixed(1)} PW`;
    } else if (watts >= 1e12) {
      return `${(watts/1e12).toFixed(1)} TW`;
    } else {
      return `${(watts/1e9).toFixed(1)} GW`;
    }
  };

  const calculateResults = () => {
    const distance = selectedStar.distance * LY_TO_M;
    
    // Mass flow rate calculation
    const massFlowRate = thrust / exhaustVelocity;
    
    // Calculate acceleration
    const initialAcceleration = thrust / dryMass;
    
    // Calculate time needed to reach cruise velocity
    const timeToVelocity = maxVelocity / initialAcceleration;
    
    // Calculate fuel needed for acceleration
    const fuelForAccel = massFlowRate * timeToVelocity;
    const totalFuelMass = 2 * fuelForAccel; // Double for deceleration
    
    // Calculate mass ratio
    const massRatio = (dryMass + totalFuelMass) / dryMass;
    
    // Calculate relativistic factors
    const gamma = 1 / Math.sqrt(1 - Math.pow(maxVelocity/C, 2));
    
    // Calculate journey times
    const accelerationDistance = 0.5 * initialAcceleration * Math.pow(timeToVelocity, 2);
    const coastDistance = distance - (2 * accelerationDistance);
    const coastTime = coastDistance / maxVelocity;
    
    const totalCoordinateTime = coastTime + (2 * timeToVelocity);
    const totalProperTime = (coastTime/gamma) + (2 * timeToVelocity/gamma);
    
    // Power calculations
    const powerOutput = (thrust * exhaustVelocity) / 2;
    const theoreticalPower = massFlowRate * 3.52e14; // D-He3 fusion energy
    
    setResults({
      acceleration: initialAcceleration / 9.8, // in g
      accelerationTime: timeToVelocity / (24 * 3600), // days
      coastTime: coastTime / YEAR_TO_SECONDS, // years
      totalTime: totalCoordinateTime / YEAR_TO_SECONDS, // years
      shipTime: totalProperTime / YEAR_TO_SECONDS, // years
      fuelMass: totalFuelMass / 1000, // tons
      massRatio: massRatio,
      peakVelocity: maxVelocity / C, // fraction of c
      gamma: gamma,
      powerOutput: powerOutput,
      theoreticalPower: theoreticalPower,
      massFlowRate: massFlowRate, // kg/s
      efficiency: (powerOutput / theoreticalPower) * 100 // percent
    });
  };

  // Recalculate when parameters change
  useEffect(() => {
    calculateResults();
  }, [dryMass, thrust, exhaustVelocity, efficiency, maxVelocity, selectedStar]);

  // Format values for display
  const dryMassKilotons = dryMass / 1000000;
  const dryMassTons = dryMass / 1000;
  const thrustMN = thrust / 1000000;
  const exhaustVelocityC = exhaustVelocity / C;
  const maxVelocityC = maxVelocity / C;

  // Reset to original Nauvoo specifications
  const resetToNauvooSpecs = () => {
    setDryMass(NAUVOO_SPECS.dryMass);
    setThrust(NAUVOO_SPECS.thrust);
    setExhaustVelocity(NAUVOO_SPECS.exhaustVelocity);
    setEfficiency(NAUVOO_SPECS.efficiency);
    setMaxVelocity(NAUVOO_SPECS.maxVelocity);
    setSelectedStar(NAUVOO_SPECS.star);
  };

  return (
    <div className="max-w-4xl mx-auto p-6 bg-zinc-900 border border-zinc-800 rounded-md shadow-lg">
      <h2 className="text-2xl font-bold text-white mb-6">Epstein Drive Interstellar Calculator v0.1</h2>
      
      <div className="grid md:grid-cols-2 gap-6">
        {/* Input Controls */}
        <div className="bg-zinc-800 p-4 rounded-md shadow border border-zinc-700">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold text-zinc-200">Ship Parameters</h2>
            <button 
              onClick={resetToNauvooSpecs}
              className="px-4 py-2 bg-sky-600 text-white text-sm font-medium rounded-sm hover:bg-sky-700 focus:outline-none focus:ring-2 focus:ring-sky-500"
            >
              Reset to Nauvoo Specs
            </button>
          </div>
          
          <div className="mb-4">
            <label className="block text-sm font-medium text-zinc-300 mb-1">
              Dry Mass: {formatNumber(dryMassTons)} tons ({formatNumber(dryMassKilotons, 2)} kilotons)
            </label>
            <input
              type="range"
              min={1000000}
              max={100000000}
              step={1000000}
              value={dryMass}
              onChange={(e) => setDryMass(Number(e.target.value))}
              className="w-full h-2 bg-zinc-700 rounded-md appearance-none cursor-pointer accent-sky-500"
            />
          </div>
          
          <div className="mb-4">
            <label className="block text-sm font-medium text-zinc-300 mb-1">
              Total Thrust: {formatNumber(thrustMN)} MN
            </label>
            <input
              type="range"
              min={10000000}
              max={1000000000}
              step={10000000}
              value={thrust}
              onChange={(e) => setThrust(Number(e.target.value))}
              className="w-full h-2 bg-zinc-700 rounded-md appearance-none cursor-pointer accent-sky-500"
            />
          </div>
          
          <div className="mb-4">
            <label className="block text-sm font-medium text-zinc-300 mb-1">
              Exhaust Velocity: {formatNumber(exhaustVelocityC * 100, 2)}% c
            </label>
            <input
              type="range"
              min={0.01 * C}
              max={0.15 * C}
              step={0.01 * C}
              value={exhaustVelocity}
              onChange={(e) => setExhaustVelocity(Number(e.target.value))}
              className="w-full h-2 bg-zinc-700 rounded-md appearance-none cursor-pointer accent-sky-500"
            />
          </div>
          
          <div className="mb-4">
            <label className="block text-sm font-medium text-zinc-300 mb-1">
              Maximum Velocity: {formatNumber(maxVelocityC * 100, 2)}% c
            </label>
            <input
              type="range"
              min={0.05 * C}
              max={0.25 * C}
              step={0.01 * C}
              value={maxVelocity}
              onChange={(e) => setMaxVelocity(Number(e.target.value))}
              className="w-full h-2 bg-zinc-700 rounded-md appearance-none cursor-pointer accent-sky-500"
            />
          </div>
          
          <div className="mb-4">
            <label className="block text-sm font-medium text-zinc-300 mb-1">
              Destination
            </label>
            <select
              value={selectedStar.name}
              onChange={(e) => setSelectedStar(STAR_SYSTEMS.find(s => s.name === e.target.value))}
              className="block w-full px-3 py-2 bg-zinc-700 border border-zinc-600 text-zinc-200 rounded-sm shadow-sm focus:outline-none focus:ring-sky-500 focus:border-sky-500"
            >
              {STAR_SYSTEMS.map(star => (
                <option key={star.name} value={star.name}>
                  {star.name} ({star.distance} light years)
                </option>
              ))}
            </select>
          </div>
        </div>
        
        {/* Results Display */}
        <div className="bg-zinc-800 p-4 rounded-md shadow border border-zinc-700">
          <h2 className="text-xl font-semibold mb-4 text-zinc-200">Journey Results</h2>
          
          {results && (
            <div className="space-y-3">
              <div className="grid grid-cols-2 gap-4">
                <div className="bg-zinc-700 p-3 rounded-md">
                  <h3 className="text-sm font-medium text-zinc-400">Total Journey Time</h3>
                  <p className="text-xl font-bold text-sky-400">{formatNumber(results.totalTime)} years</p>
                </div>
                
                <div className="bg-zinc-700 p-3 rounded-md">
                  <h3 className="text-sm font-medium text-zinc-400">Ship Time</h3>
                  <p className="text-xl font-bold text-sky-400">{formatNumber(results.shipTime)} years</p>
                </div>
              </div>
              
              <div className="border-t border-zinc-700 pt-3">
                <h3 className="font-medium text-zinc-300 mb-2">Performance Details</h3>
                <ul className="space-y-1 text-sm">
                  <li className="flex justify-between">
                    <span className="text-zinc-400">Acceleration:</span>
                    <span className="font-medium text-zinc-200">{formatNumber(results.acceleration, 2)} g</span>
                  </li>
                  <li className="flex justify-between">
                    <span className="text-zinc-400">Acceleration Phase:</span>
                    <span className="font-medium text-zinc-200">{formatNumber(results.accelerationTime)} days</span>
                  </li>
                  <li className="flex justify-between">
                    <span className="text-zinc-400">Coast Phase:</span>
                    <span className="font-medium text-zinc-200">{formatNumber(results.coastTime)} years</span>
                  </li>
                  <li className="flex justify-between">
                    <span className="text-zinc-400">Time Dilation Factor:</span>
                    <span className="font-medium text-zinc-200">{results.gamma.toFixed(3)}</span>
                  </li>
                </ul>
              </div>
              
              <div className="border-t border-zinc-700 pt-3">
                <h3 className="font-medium text-zinc-300 mb-2">Fuel Requirements</h3>
                <ul className="space-y-1 text-sm">
                  <li className="flex justify-between">
                    <span className="text-zinc-400">Fuel Mass:</span>
                    <span className="font-medium text-zinc-200">{formatNumber(results.fuelMass)} tons</span>
                  </li>
                  <li className="flex justify-between">
                    <span className="text-zinc-400">Mass Ratio:</span>
                    <span className="font-medium text-zinc-200">{results.massRatio.toFixed(2)}</span>
                  </li>
                  <li className="flex justify-between">
                    <span className="text-zinc-400">Mass Flow Rate:</span>
                    <span className="font-medium text-zinc-200">{formatNumber(results.massFlowRate, 1)} kg/s</span>
                  </li>
                </ul>
              </div>
              
              <div className="border-t border-zinc-700 pt-3">
                <h3 className="font-medium text-zinc-300 mb-2">Power Systems</h3>
                <ul className="space-y-1 text-sm">
                  <li className="flex justify-between">
                    <span className="text-zinc-400">Power Output:</span>
                    <span className="font-medium text-zinc-200">{formatPower(results.powerOutput)}</span>
                  </li>
                  <li className="flex justify-between">
                    <span className="text-zinc-400">Theoretical Power:</span>
                    <span className="font-medium text-zinc-200">{formatPower(results.theoreticalPower)}</span>
                  </li>
                  <li className="flex justify-between">
                    <span className="text-zinc-400">Drive Efficiency:</span>
                    <span className="font-medium text-zinc-200">{formatNumber(results.efficiency, 3)}%</span>
                  </li>
                </ul>
              </div>
            </div>
          )}
        </div>
      </div>
      
      <div className="mt-6 text-sm text-zinc-400">
        <p>Based on the Epstein Drive from The Expanse universe. Uses relativistic calculations for high-velocity travel.</p>
      </div>
    </div>
  );
};

export default EpsteinDriveCalculator;