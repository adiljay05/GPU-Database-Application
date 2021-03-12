class GPU_info:
    def __init__(self, name,manufacturer,issued_date,geometryShader,tesselationShader,
    shaderInt16,sparseBinding,textureCompressionETC2,vertexPipelineStoresAndAtomics): 
        self.name = name
        self.manufacturer = manufacturer
        self.issued_date = issued_date
        self.geometryShader = geometryShader
        self.tesselationShader = tesselationShader
        self.shaderInt16 = shaderInt16
        self.sparseBinding = sparseBinding
        self.textureCompressionETC2 = textureCompressionETC2
        self.vertexPipelineStoresAndAtomics = vertexPipelineStoresAndAtomics
