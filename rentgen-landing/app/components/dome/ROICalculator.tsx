'use client';

import { useState, useMemo } from 'react';

type Model = {
    id: 'pod',
    name: 'Eco Pod',
    cost: 25000,
    area: '35m²',
    defaultRate: 120
};

const MODELS: Model[] = [
    { id: 'pod', name: 'Eco Pod', cost: 25000, area: '35m²', defaultRate: 120 },
    { id: 'hive', name: 'Family Hive', cost: 65000, area: '90m²', defaultRate: 250 },
    { id: 'estate', name: 'Luxe Estate', cost: 180000, area: '250m²', defaultRate: 800 }
];

export default function ROICalculator() {
    const [selectedModel, setSelectedModel] = useState<Model>(MODELS[0]);
    const [nightlyRate, setNightlyRate] = useState<number>(MODELS[0].defaultRate);
    const [occupancy, setOccupancy] = useState<number>(65); // Default 65%

    const stats = useMemo(() => {
        const annualRevenue = nightlyRate * 365 * (occupancy / 100);
        const monthlyRevenue = annualRevenue / 12;
        const paybackMonths = selectedModel.cost / monthlyRevenue;
        const paybackYears = paybackMonths / 12;
        const roi = (annualRevenue / selectedModel.cost) * 100;

        return {
            monthly: Math.round(monthlyRevenue),
            annual: Math.round(annualRevenue),
            paybackYears: paybackYears.toFixed(1),
            roi: Math.round(roi)
        };
    }, [selectedModel, nightlyRate, occupancy]);

    const handleModelChange = (model: Model) => {
        setSelectedModel(model);
        setNightlyRate(model.defaultRate);
    };

    return (
        <section className="py-24 px-6 bg-black text-white">
            <div className="max-w-4xl mx-auto space-y-12">
                <div className="text-center space-y-4">
                    <h2 className="text-3xl md:text-5xl font-black uppercase tracking-tighter">The Math of Airform</h2>
                    <p className="text-gray-400 font-mono text-sm max-w-lg mx-auto">
                        Don't trust emotions. Trust the numbers. Calculate your return on investment based on real market data.
                    </p>
                </div>

                <div className="grid md:grid-cols-2 gap-12 bg-[#111] p-8 md:p-12 rounded-3xl border border-white/10 shadow-2xl">

                    {/* CONTROLS */}
                    <div className="space-y-10">
                        {/* Model Selector */}
                        <div className="space-y-4">
                            <label className="text-xs font-mono uppercase text-gray-400 tracking-widest">Select Model</label>
                            <div className="grid grid-cols-3 gap-2">
                                {MODELS.map(model => (
                                    <button
                                        key={model.id}
                                        onClick={() => handleModelChange(model)}
                                        className={`py-3 px-2 rounded-xl text-sm font-bold transition-all border ${selectedModel.id === model.id
                                                ? 'bg-white text-black border-white'
                                                : 'bg-black text-gray-500 border-white/10 hover:border-white/30'
                                            }`}
                                    >
                                        {model.name}
                                    </button>
                                ))}
                            </div>
                            <div className="text-right text-xs font-mono text-gray-500">
                                Base Cost: ${selectedModel.cost.toLocaleString()}
                            </div>
                        </div>

                        {/* Sliders */}
                        <div className="space-y-6">

                            {/* Nightly Rate */}
                            <div className="space-y-2">
                                <div className="flex justify-between items-end">
                                    <label className="text-xs font-mono uppercase text-gray-400 tracking-widest">Nightly Rate</label>
                                    <span className="text-2xl font-bold font-mono">${nightlyRate}</span>
                                </div>
                                <input
                                    type="range"
                                    min="30"
                                    max="1500"
                                    step="10"
                                    value={nightlyRate}
                                    onChange={(e) => setNightlyRate(Number(e.target.value))}
                                    className="w-full h-2 bg-gray-800 rounded-lg appearance-none cursor-pointer accent-white"
                                />
                            </div>

                            {/* Occupancy */}
                            <div className="space-y-2">
                                <div className="flex justify-between items-end">
                                    <label className="text-xs font-mono uppercase text-gray-400 tracking-widest">Occupancy Rate</label>
                                    <span className="text-2xl font-bold font-mono">{occupancy}%</span>
                                </div>
                                <input
                                    type="range"
                                    min="0"
                                    max="100"
                                    step="5"
                                    value={occupancy}
                                    onChange={(e) => setOccupancy(Number(e.target.value))}
                                    className="w-full h-2 bg-gray-800 rounded-lg appearance-none cursor-pointer accent-white"
                                />
                                <div className="flex justify-between text-[10px] uppercase text-gray-600 font-mono pt-1">
                                    <span>Conserv</span>
                                    <span>Average</span>
                                    <span>Boom</span>
                                </div>
                            </div>

                        </div>
                    </div>

                    {/* RESULTS */}
                    <div className="flex flex-col justify-center space-y-8 pl-0 md:pl-8 border-l-0 md:border-l border-white/10">

                        <div className="space-y-1">
                            <div className="text-xs font-mono uppercase text-gray-500 tracking-widest">Annual Revenue</div>
                            <div className="text-4xl md:text-5xl font-black tracking-tight text-white">
                                ${stats.annual.toLocaleString()}
                            </div>
                            <div className="text-sm text-gray-400">
                                ${stats.monthly.toLocaleString()} / mo
                            </div>
                        </div>

                        <div className="grid grid-cols-2 gap-6">
                            <div className="p-4 bg-white/5 rounded-2xl border border-white/5">
                                <div className="text-[10px] font-mono uppercase text-gray-500 mb-1">Payback Period</div>
                                <div className="text-2xl font-bold text-white">
                                    {stats.paybackYears} <span className="text-sm font-normal text-gray-400">Years</span>
                                </div>
                            </div>
                            <div className="p-4 bg-green-500/10 rounded-2xl border border-green-500/20">
                                <div className="text-[10px] font-mono uppercase text-green-400 mb-1">Annual ROI</div>
                                <div className="text-2xl font-bold text-green-400">
                                    {stats.roi}%
                                </div>
                            </div>
                        </div>

                    </div>

                </div>
            </div>
        </section>
    );
}
