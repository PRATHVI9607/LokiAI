import { describe, it, expect } from "vitest";
import { providerLabel, rewardToPct, formatLatency } from "./format";

describe("providerLabel", () => {
  it("maps known providers to friendly labels", () => {
    expect(providerLabel("fast_path")).toBe("instant");
    expect(providerLabel("ollama")).toBe("local");
    expect(providerLabel("openrouter:google/gemma")).toBe("openrouter");
  });
  it("passes through unknown providers and empties", () => {
    expect(providerLabel("nvidia")).toBe("nvidia");
    expect(providerLabel("")).toBe("");
  });
});

describe("rewardToPct", () => {
  it("clamps to the 2–100 range", () => {
    expect(rewardToPct(-5)).toBe(2);
    expect(rewardToPct(10)).toBe(100);
  });
  it("maps mid reward proportionally", () => {
    // reward 0.5 → ((0.5+0.5)/2)*100 = 50
    expect(rewardToPct(0.5)).toBeCloseTo(50);
  });
});

describe("formatLatency", () => {
  it("uses ms under a second and seconds above", () => {
    expect(formatLatency(840)).toBe("840ms");
    expect(formatLatency(1840)).toBe("1.8s");
  });
  it("guards bad input", () => {
    expect(formatLatency(-1)).toBe("—");
    expect(formatLatency(NaN)).toBe("—");
  });
});
