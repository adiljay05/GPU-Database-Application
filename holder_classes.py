class GPU_info:
    def __init__(self, name,manufacturer,issued_date,geometryShader,tesselationShader,
    shaderInt16,sparseBinding,textureCompressionETC2,vertexPipelineStoresAndAtomics): 
        self.name = name
        self.manufacturer = manufacturer
        self.issued_date = issued_date
        
        if geometryShader == 'True':
            self.geometryShader = True
        else:
            self.geometryShader = False
        
        if tesselationShader == 'True':
            self.tesselationShader = True
        else:
            self.tesselationShader = False
        
        if shaderInt16 == 'True':
            self.shaderInt16 = True
        else:
            self.shaderInt16 = False
        
        if sparseBinding == 'True':
            self.sparseBinding = True
        else:
            self.sparseBinding = False
        
        if textureCompressionETC2 == 'True':
            self.textureCompressionETC2 = True
        else:
            self.textureCompressionETC2 = False
        
        if vertexPipelineStoresAndAtomics == 'True':
            self.vertexPipelineStoresAndAtomics = True
        else:
            self.vertexPipelineStoresAndAtomics = False
