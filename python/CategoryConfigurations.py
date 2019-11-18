#Brief configuration file for creating categories in the models
print("Loading Categories...")

tt_Categories = {'cat0':'tt_0jet',
                 'cat1':'tt_boosted_onejet',
                 'cat2':'tt_boosted_multijet',
                 'cat3':'tt_vbf_lowHpT',
                 'cat4':'tt_vbf_highHpT'}
mt_Categories = {'mt_0jet_PTH_0_10':'mt_0jet_PTH_0_10',
                 'mt_0jet_PTH_GE10':'mt_0jet_PTH_GE10',
                 'mt_vbf_PTH_0_200':'mt_vbf_PTH_0_200',
                 'mt_vbf_PTH_GE_200':'mt_vbf_PTH_GE_200',
                 'mt_boosted_1J':'mt_boosted_1J',
                 'mt_boosted_GE2J':'mt_boosted_GE2J'}
et_Categories = {'et_0jet_PTH_0_10':'et_0jetlow',
                 'et_0jet_PTH_GE10':'et_0jethigh',
                 'et_vbf_PTH_0_200':'et_vbflow',
                 'et_vbf_PTH_GE_200':'et_vbfhigh',
                 'et_boosted_1J':'et_boosted1',
                 'et_boosted_GE2J':'et_boosted2'}
em_Categories = {'em_0jet_PTH_0_10':'em_0jetlow',
                 'em_0jet_PTH_GE10':'em_0jethigh',
                 'em_vbf_PTH_0_200':'em_vbflow',
                 'em_vbf_PTH_GE_200':'em_vbfhigh',
                 'em_boosted_1J':'em_boosted1',
                 'em_boosted_GE2J':'em_boosted2'}
Categories = {'tt':tt_Categories,
              'mt':mt_Categories,
              'et':et_Categories,
              'em':em_Categories}
