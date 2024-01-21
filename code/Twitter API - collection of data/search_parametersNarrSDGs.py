#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 09:59:20 2020
@author: carlotatarazonalizarraga and emeros
"""

##SEARCH PARAMETER, in this case the parameters are searching for tweets that contains for example the words 'modern energy'
# this means that it will look for tweets that contains the words 'modern' and 'energy' but not necessary in togheter and that order!


#Corporations
keywords_sdg7 = ['affordable energy', 'reliable energy', 'modern energy','access to energy','electrification','clean energy','renewable energy','energy efficiency','renewables','energy infrastructure','fossil-fuel technology','clean energy','international cooperation on energy','alternative energy','energy resources','solar energy','photovoltaic','photovoltaics','electrification','bioenergy','biofuel','biofuels','biodiesel','biogasoline','carbon','charcoal','green energy','biomass','woodfuels','sustainable energy','sustainable energy investments','energy developing countries','energy land-locked countries','energy least developed countries']



keywords_sdg11 = ['safe housing','affordable housing','upgrade slums','sustainable transport','sustainable transportation','public transport','city air quality','waste management','sustainable cities and communities','sustainable housing','urbanization','urban enviromental impact','climate policy','footprint','green space','green spaces','household energy','household resilience','resilience','household fuels','human activity enviroment','human resource planning','human sensors','mega cities','megacities','neighborhood sustainability assessment','population surveillance','smart cities','smart city','enviromental inequality','waste management','national development planning','regional development planning','sustainable rural development','city pollution','city mitigation','city adaptation climate change','city resilience','resilient buildings','sustainable buildings','buildings local materials','sustainable urbanization','sustainable construction']

keywords_sdg13 = ['climate resilience','natural disasters','climate hazard','climate hazards','climate impact','climate mitigation','climate policy','climate policies','climate action','climate change strategies','climate planning','climate national','climate international', 'climate change','climate-related hazards', 'COP', 'COP26','COP25','greenhouse gas', 'gas emission', 'scoail footprint', 'sustainable footprint','biosequestration','carbon footprint','carbon emission','carbon economuy','carbon storage', 'carbon sequestration','global warming','emissions','enviromental change','co2 capture','climate variability','climate refugees','climate biodiversity','climate desertification','climate change developed countries','Paris Agreement','climate change marginalized communities','UNFCC','negotiation global response climate change', 'global warming commitment']

keywords_new = ['carbon dioxide emissons', 'fossil fuels', 'fossil fuel', 'coal-fired power station', 'coal-fired power stations', 'coal-fired power plants', 'coal-fired power plant', 'coal power plants', 'nuclear power', 'bioenergy', 'wind power', 'solar energy', 'wiind power', 'fossil fuel', 'oil refinery', 'oil platforms', 'gaasoline', 'electrical cars', 'flooding', 'climate-related flooding']

keywords = keywords_sdg7 + keywords_sdg13 + keywords_sdg11

ub_name = None
