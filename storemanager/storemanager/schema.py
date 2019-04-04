import graphene

from products.models import Product


class ProductType(graphene.ObjectType):
    name = graphene.String(description='The name of the product')
    category = graphene.String(description='The category of the product')
    
class QueryType(graphene.ObjectType):
    all_products = graphene.List(ProductType, description='A few billion products')
    product = graphene.Field(
        ProductType,
        id=graphene.ID(),
        description='A product belonging to a given id'
    )

    def resolve_all_products(self, args,):
        return Product.objects.all()

    def resolve_product(self, args, context, info):
        id = args.get('id')
        return Product.objects.get(pk=id)

schema = graphene.Schema(query=QueryType)

