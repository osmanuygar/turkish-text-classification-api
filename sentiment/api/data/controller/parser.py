from flask_restplus import reqparse

pagination_arguments = reqparse.RequestParser()
pagination_arguments.add_argument('page', type=int, required=False, default=1, help='Page number')
pagination_arguments.add_argument('bool', type=bool, required=False, default=1, help='Page number')
pagination_arguments.add_argument('per_page', type=int, required=False, choices=[2, 10, 20, 30, 40, 50],
                                  default=10, help='Results per page')

pagination_arguments_with_model = reqparse.RequestParser()
pagination_arguments_with_model.add_argument('model', type=str, required=True, default=1, help='model')
pagination_arguments_with_model.add_argument('page', type=int, required=False, default=1, help='Page number')
pagination_arguments_with_model.add_argument('bool', type=bool, required=False, default=1, help='Page number')
pagination_arguments_with_model.add_argument('per_page', type=int, required=False, choices=[2, 10, 20, 30, 40, 50],
                                  default=10, help='Results per page')

pagination_arguments_with_category = reqparse.RequestParser()
pagination_arguments_with_category.add_argument('category', type=str, required=True, default=1, help='category')
pagination_arguments_with_category.add_argument('page', type=int, required=False, default=1, help='Page number')
pagination_arguments_with_category.add_argument('bool', type=bool, required=False, default=1, help='Page number')
pagination_arguments_with_category.add_argument('per_page', type=int, required=False, choices=[2, 10, 20, 30, 40, 50],
                                  default=10, help='Results per page')
