function ColumType() {
    this.commIntType = ['int8','int16','int','int32','integer','int64']
    this.commType = this.commIntType.concat(['float','float32','float','double','float64','float16','bfloat16'])
    this.Default = ['default']
    this.Numeric = this.commType
    this.String = ['string']
    this.DenseVector = this.commType
    this.SparseVector = this.commType
    this.SparseVectorIndices = this.commIntType
    this.FLOAT = 2;
    this.STRING = 3; 
}

export default {
    ColumType
};