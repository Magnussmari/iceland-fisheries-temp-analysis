# CLAUDE.md - Project-Specific Instructions

## Project Context

This is a data visualization and demonstration project supporting a presentation on **Icelandic Fisheries Resilience**. The presentation focuses on integrated challenges facing the industry and how AI/data-driven solutions can address them.

## Primary Objectives

1. Create compelling data visualizations that illustrate key points from the presentation
2. Demonstrate how different data sources (fishing, processing, ecosystem) can be integrated
3. Show practical AI/ML applications for fisheries management
4. Support the argument that modern resilience = adaptability, not just biomass

## Domain Knowledge

### Key Icelandic Terms
- **Loðna** = Capelin (crucial forage fish)
- **Þorskur** = Cod (most valuable commercial species)
- **Hafrannsóknastofnun** = Marine Research Institute
- **Kvóti** = Quota
- **Burðarþol** = Resilience/carrying capacity

### Critical Data Points from Research

1. **Capelin Crisis**: Stock moving toward Greenland, zero fishing quota recommended for 2024/2025
2. **Cod Condition**: Declining condition index, reduced liver weight due to lack of capelin prey
3. **Export Patterns**: Norway receives 20% of volume but only 11% of value (unprocessed fish)
4. **Technology Risk**: Skaginn 3X bankruptcy affects most major processing plants

## Visualization Priorities

When creating visualizations, focus on:

1. **Ecological Trends**
   - Stock movement patterns
   - Condition indices over time
   - Temperature correlations

2. **Economic Impacts**
   - Value per ton by market
   - Processing vs. unprocessed export ratios
   - Cost pressures over time

3. **Integration Opportunities**
   - How vessel data + processing data + ecosystem data create insights
   - Real-time quality optimization examples
   - Predictive modeling possibilities

## Data Handling Guidelines

### Available Data Sources
- Use publicly available data from Hagstofa Íslands (Statistics Iceland)
- Reference data from Hafrannsóknastofnun reports
- Create synthetic/example data when real data not available for demonstration purposes

### When Creating Synthetic Data
- Base on realistic ranges from the presentation document
- Clearly label as "example/demonstration data"
- Maintain proportions and trends consistent with cited research

## Code Standards

- Use Python for data analysis and visualization
- Prefer libraries: pandas, matplotlib, seaborn, plotly (for interactive)
- Include clear comments in Icelandic or English
- Make visualizations publication-ready (clear labels, legends, titles)

## Communication Style

- Use both Icelandic and English as appropriate
- Technical terms should be explained when first introduced
- Focus on actionable insights, not just descriptive statistics
- Connect every visualization back to the presentation's core argument

## AI/ML Integration Examples

When demonstrating AI capabilities, focus on:

1. **Real-time Quality Mapping**
   - Linking vessel location → catch quality → processing yield
   - Example: "Fish from area X shows 15% lower condition index"

2. **Passive Ecosystem Monitoring**
   - Using fleet movements as ecosystem sensors
   - Pattern recognition in fishing behavior

3. **Value Optimization**
   - Market matching based on quality/size/timing
   - Avoiding the "Norway trap" (low-value bulk export)

## Specific Tasks Support

### For Data Visualization Tasks
- Prioritize clarity and impact over complexity
- Use Icelandic labels for presentation slides
- Include source citations
- Make charts colorblind-friendly

### For Analysis Tasks
- Connect findings to specific sections of the presentation
- Quantify impacts where possible (e.g., "15% reduction in yield")
- Highlight integration opportunities

### For AI/ML Demonstrations
- Show realistic use cases, not sci-fi scenarios
- Address the "trust" theme from the sub-presentation
- Demonstrate how AI empowers experts rather than replacing them

## Arctic Tracker MCP Integration

This project has access to Arctic species data through MCP tools. Use these for:
- Conservation status of Icelandic fish species
- CITES trade data for context on international fisheries
- Threat analysis for species mentioned in presentation

Relevant species to research:
- Capelin (Mallotus villosus)
- Atlantic cod (Gadus morhua)
- Other key Icelandic commercial species

## Success Criteria

A successful data demonstration should:
1. Clearly illustrate one of the presentation's key arguments
2. Be understandable to non-technical fisheries stakeholders
3. Suggest actionable insights (not just describe problems)
4. Show integration potential across data silos
5. Support the "adaptability as resilience" thesis

## Notes

- The presentation targets fisheries industry professionals, policymakers, and researchers
- Balance scientific rigor with accessibility
- Icelandic fisheries context is unique (quota system, small population, geographic isolation)
- Climate change impacts are immediate and observable, not theoretical

## References Available

All 22 cited sources from the presentation document are available. When creating visualizations or analysis, cite relevant sources and maintain consistency with published data.