export interface StudyList {
  id: string;
  title: string;
  description: string;
  image: string;
  pub_date: string;
  end_date: string;
}

export interface Study extends StudyList {
  ui: string;
  length: number;
  index: number;
}
