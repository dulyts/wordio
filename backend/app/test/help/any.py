class Any(object):
	def __init__(self, **kwargs):
		self.__dict__ = kwargs
		