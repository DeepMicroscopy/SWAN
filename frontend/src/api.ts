export interface StudyList {
  id: string;
  title: string;
  description: string;
  image: string;
  pub_date: string;
  end_date: string;
}

export interface StudyDetail extends StudyList {
  ui: Ui;
  length: number;
  index: number;
}

export interface Ui {
  title: string;
  labels: UiLabels;
}

export interface UiLabels {
  left: UiDirection;
  right: UiDirection;
  up?: UiDirection;
  down?: UiDirection;
}

export interface UiDirection {
  text: string;
}
