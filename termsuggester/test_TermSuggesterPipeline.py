#!/usr/bin/env python
################################################################################
#    Created by Oscar Martinez                                                 #
#    o.rubi@esciencecenter.nl                                                  #
################################################################################

import unittest
from TermSuggestionsAggregator import TermSuggestionsAggregator, Aggregation
from elsearch import ELSearch
from wnsearch import WNSearch
from precomputed import PrecomputedClusterSuggester

class TermSuggesterPipelineTestCase(unittest.TestCase):
    """Tests for `TermSuggester.py`."""

    def test_0_initialize_WNSearch(self): #The _0_ is added to guarantee it is the first executed test
        """Test that the WNSearch method is properly intialized"""
        WNSearch()
        
    def test_0_initialize_ELSearch(self): 
        """Test that the ELSearch method is properly intialized"""
        ELSearch()
        
    def test_0_initialize_PrecomputedClusterSuggester(self): 
        """Test that the ELSearch method is properly intialized"""    
        PrecomputedClusterSuggester()

    def test_getSuggestionsAvg(self):
        """Test that the term suggestion works with ElasticSearch and WordNet with Average as aggregation method"""
        methods = (WNSearch(), ELSearch(),PrecomputedClusterSuggester())
        ts = TermSuggestionsAggregator()

        d1 = {u'renting': 0.032297780366267945, u'5000838': 0.03256212510711225, u"alamo's": 0.05313331194581711, 
              u'car': 1.0, u'travel': 0.041410107688661484, u'motor_vehicle': 1.0, u'airlines': 0.03910270828569188, 
              u'cable_car': 1.0, u'collision': 0.03310312727459771, u'airport': 0.03430880515161479, 
              u'wheeled_vehicle': 1.0, u'rent': 0.06008558630654296, u'cars': 0.0509548717589492, 
              u'traveler': 0.0377490146083934, u"national's": 0.05402044828276183, u'compartment': 1.0, 
              u'rental': 0.12375781253024692, u'fares': 0.040019352962099373, u'blackout': 0.03228453772324515}
        d2 = ts.getSuggestions('car', methods, Aggregation.Average)
        self.assertEqual(d1,d2)
        
    def test_getSuggestionsSum(self):
        """Test that the term suggestion works with ElasticSearch and WordNet with SumMethod as aggragation"""
        methods = (WNSearch(), ELSearch(), PrecomputedClusterSuggester())
        ts = TermSuggestionsAggregator()
        
        d1 = {u'renting': 0.032297780366267945, u'5000838': 0.03256212510711225, u"alamo's": 0.05313331194581711, 
              u'car': 2.0, u'travel': 0.041410107688661484, u'motor_vehicle': 1, u'airlines': 0.03910270828569188, 
              u'cable_car': 1, u'collision': 0.03310312727459771, u'airport': 0.03430880515161479, 
              u'wheeled_vehicle': 1, u'rent': 0.06008558630654296, u'cars': 0.0509548717589492, 
              u'traveler': 0.0377490146083934, u"national's": 0.05402044828276183, u'compartment': 1, 
              u'rental': 0.12375781253024692, u'fares': 0.040019352962099373, u'blackout': 0.03228453772324515}
        d2 = ts.getSuggestions('car', methods, Aggregation.Sum)
        self.assertEqual(d1,d2)
if __name__ == '__main__':
    unittest.main()
