class Config:
  def __init__(self):
    self.HOST            = '0.0.0.0'
    self.PORT            = 8000
    self.GENERATOR       = 'Project/static/database/generator.txt'
    self.KEY             = 'this_is_a_secret_key'
    self.DATABASE        = 'Project/static/database/main.db'
    self.TESTDATABASE    = 'Project/static/database/test.db'
    self.CURRENTDATABASE = self.DATABASE
    self.FEEDBACK_IMAGES = "/home/runner/ClassProject1-1/Project/static/images/feedback"
    self.PROFILE_IMAGES  = "/home/runner/ClassProject1-1/Project/static/images/profile"
    self.SPECIAL_IMAGES  = "/home/runner/ClassProject1-1/Project/static/images/menu/special"